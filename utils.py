import numpy as np

'''
    This is used to evaluate the performance of a binary classification map against a truth image
    The class LoggerWriter is used to log messages
'''

class LoggerWriter:
    def __init__(self, logfct):
        self.logfct = logfct
        self.buf = []

    def write(self,msg):
        if msg.endswith('\n'):
            self.buf.append(msg.rstrip('\n'))
            self.logfct(''.join(self.buf))
            self.buf = []

        else:
            self.buf.append(msg)

    def flush(self):
        pass

# Calculates performance metrics for a binary classification task based on comparing
# a predicted binary map with a ground truth image

def score_card(input_map, groundtruth_img, threshold = 0.5):
    binary_map = input_map
    binary_map[binary_map < threshold] = 0
    binary_map[binary_map == threshold] = 0
    binary_map[binary_map > threshold] = 1
    [rows, cols] = groundtruth_img.shape
    '''
        TP (True Positives) --> Predicted 1 (positive) and ground truth is also 1.
        FP (False Positives) --> Predicted 1 but ground truth is 0.
        TN (True Negatives) --> Predicted 0 and ground truth is also 0.
        FN (False Negatives) --> Predicted 0 but ground truth is 1.
    '''
    TP, FP, TN, FN = 0, 0, 0, 0

    for i in range (rows):
        for j in range(cols):
            if groundtruth_img[i,j]== 1 and binary_map[i,j]==1:
                TP = TP +1
            elif groundtruth_img[i,j] == 0 and binary_map[i,j]==1:
                FP = FP +1
            elif groundtruth_img[i, j] == 0 and binary_map[i, j] == 0:
                TN = TN + 1
            elif groundtruth_img[i,j] == 1 and binary_map[i,j]==0:
                FN = FN +1
    '''
        Precision --> Measures how many of the predicted positives (1s) were actually correct (True Positives).
        Recall --> Measures how many of the actual positives (ground truth 1s) were correctly predicted.
        FScore --> A harmonic mean of precision and recall, used as an overall performance measure.
    '''
    precision = float(TP)/ float(TP + FP)
    recall = float(TP) / float(TP + FN)
    fScore = float(2*precision*recall)/float(precision + recall)

    error_count = 0
    for i in range(rows):
        for j in range(cols):
            if groundtruth_img[i,j] != binary_map[i,j]:
                error_count+= 1

    error_rate = float(error_count)/ float(rows*cols)

    return precision, recall, fScore, error_rate