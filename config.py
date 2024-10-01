import os
print(os.getcwd())
IMAGES_DIR = "/Users/weijithwimalasiri/Desktop/UoM_S5/CS3283_Embedded_Systems_Project/Project/src/data/swinyseg/images"
MASKS_DIR = "/Users/weijithwimalasiri/Desktop/UoM_S5/CS3283_Embedded_Systems_Project/Project/src/data/swinyseg/GTmaps"
RESIZE_SIZE = (300, 300)
CROP_SIZE = (288, 288)
LOG_DIR = "/Users/weijithwimalasiri/Desktop/UoM_S5/CS3283_Embedded_Systems_Project/Project/logs"
WEIGHTS_DIR = "/Users/weijithwimalasiri/Desktop/UoM_S5/CS3283_Embedded_Systems_Project/Project/weights"
INFERENCE_DIR = "/Users/weijithwimalasiri/Desktop/UoM_S5/CS3283_Embedded_Systems_Project/Project/inference"
NUM_CLASSES = 2
BATCH_SIZE = 2
INITIAL_LEARNING_RATE = 0.0001
EPOCHS = 300
SEED = 42
TEST_SIZE = 0.2

COLOR_VALUES = {0:[0,0,255],
                1:[255,255,255]}

