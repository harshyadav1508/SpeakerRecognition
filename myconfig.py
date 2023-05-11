# This file has the configurations of the experiments.

# Path of downloaded LibriSpeech datasets.
TRAIN_DATA_DIR = "/home/quan/Code/github/SpeakerRecognitionFromScratch/data/LibriSpeech/train-clean-100"
TEST_DATA_DIR = "/home/quan/Code/github/SpeakerRecognitionFromScratch/data/LibriSpeech/test-clean"

# Number of MFCCs for librosa.feature.mfcc.
N_MFCC = 40

# Hidden size of LSTM layers.
LSTM_HIDDEN_SIZE = 64

# Number of LSTM layers.
LSTM_NUM_LAYERS = 3

# Sequence length for LSTM.
SEQ_LEN = 100  # 3.2 seconds

# Alpha for the triplet loss.
TRIPLET_ALPHA = 0.1
