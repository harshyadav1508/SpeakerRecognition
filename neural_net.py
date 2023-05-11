import os
import time
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np

import feature_extraction
import myconfig


class SpeakerEncoder(nn.Module):

    def __init__(self):
        super(SpeakerEncoder, self).__init__()
        # Define the LSTM network.
        self.lstm = nn.LSTM(
            input_size=myconfig.N_MFCC,
            hidden_size=myconfig.LSTM_HIDDEN_SIZE,
            num_layers=myconfig.LSTM_NUM_LAYERS,
            batch_first=True)

    def forward(self, x):
        h0 = torch.zeros(
            myconfig.LSTM_NUM_LAYERS, x.shape[0],  myconfig.LSTM_HIDDEN_SIZE)
        c0 = torch.zeros(
            myconfig.LSTM_NUM_LAYERS, x.shape[0], myconfig.LSTM_HIDDEN_SIZE)
        y, (hn, cn) = self.lstm(x, (h0, c0))
        return y


def get_triplet_loss(anchor, pos, neg):
    """Triplet loss defined in https://arxiv.org/pdf/1705.02304.pdf."""
    cos = nn.CosineSimilarity(dim=0, eps=1e-6)
    return torch.maximum(
        cos(anchor, neg) - cos(anchor, pos) + myconfig.TRIPLET_ALPHA,
        torch.tensor(0.0))


def get_triplet_loss_from_batch_output(batch_output, batch_size):
    """Triplet loss from N*(a|p|n) batch output."""
    triplet_losses = []
    for i in range(batch_size):
        single_triplet_loss = get_triplet_loss(
            batch_output[i * 3, :],
            batch_output[i * 3 + 1, :],
            batch_output[i * 3 + 2, :])
        triplet_losses.append(single_triplet_loss)
    loss = torch.mean(torch.stack(triplet_losses))
    return loss


def train_network(num_steps, saved_model=None):
    start_time = time.time()
    losses = []
    spk_to_utts = feature_extraction.get_spk_to_utts(myconfig.TRAIN_DATA_DIR)

    encoder = SpeakerEncoder().to(myconfig.DEVICE)

    # Train
    optimizer = optim.Adam(encoder.parameters(), lr=myconfig.LEARNING_RATE)
    print("Start training")
    for step in range(num_steps):
        optimizer.zero_grad()

        # Build batched input.
        batch_input = feature_extraction.get_batched_triplet_input(
            spk_to_utts, myconfig.BATCH_SIZE).to(myconfig.DEVICE)

        # Compute loss.
        batch_output = encoder(batch_input)[:, -1, :]
        loss = get_triplet_loss_from_batch_output(
            batch_output, myconfig.BATCH_SIZE)
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
        print("step:", step, "loss:", loss.item())

    training_time = time.time() - start_time
    print("finished training in", training_time, "seconds")
    if saved_model is not None:
        os.makedirs(os.path.dirname(saved_model), exist_ok=True)
        torch.save({"encoder_state_dict": encoder.state_dict(),
                    "losses": losses,
                    "training_time": training_time},
                   saved_model)
    return losses


def run_training():
    losses = train_network(50000, myconfig.SAVED_MODEL_PATH)
    plt.plot(losses)
    plt.xlabel("step")
    plt.ylabel("loss")
    plt.show()


if __name__ == "__main__":
    run_training()
