# This file has the configurations of the experiments.

# Path of downloaded LibriSpeech datasets.
TRAIN_DATA_DIR = "/home/quan/Code/github/SpeakerRecognitionFromScratch/data/LibriSpeech/train-clean-100"
TEST_DATA_DIR = "/home/quan/Code/github/SpeakerRecognitionFromScratch/data/LibriSpeech/test-clean"

# Path of save model.
SAVED_MODEL_PATH = "/home/quan/Code/github/SpeakerRecognitionFromScratch/saved_model/saved_model.pt"

# Number of MFCCs for librosa.feature.mfcc.
N_MFCC = 40

# Hidden size of LSTM layers.
LSTM_HIDDEN_SIZE = 64

# Number of LSTM layers.
LSTM_NUM_LAYERS = 3

# Sequence length of the sliding window for LSTM.
SEQ_LEN = 100  # 3.2 seconds

# Sliding window step for LSTM inference.
SLIDING_WINDOW_STEP = 50  # 1.6 seconds

# Alpha for the triplet loss.
TRIPLET_ALPHA = 0.1

# How many triplets do we train in a single batch.
BATCH_SIZE = 8

# Learning rate.
LEARNING_RATE = 0.0001

# Number of triplets to evaluate for computing Equal Error Rate (EER).
NUM_EVAL_TRIPLETS = 1000
