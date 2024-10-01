import sys
sys.path.append("/Users/weijithwimalasiri/Desktop/UoM_S5/CS3283_Embedded_Systems_Project/Project/src")
import os
#Importing the module config
from config import *
from sklearn.model_selection import train_test_split
import albumentations as A
import tensorflow as tf
from utils import *
import numpy as np
import cv2

# Augmentation of the training data set
train_augment = A.Compose([
    A.RandomCrop(height= CROP_SIZE[0], width=CROP_SIZE[1],p=1),
    # Apply Contrast Limited Adaptive Histogram Equalization to enhance image contrast
    A.CLAHE(p=0.5),
    A.RandomGamma(p=0.5),
    A.OneOf([
        A.VerticalFlip(p=0.25),
        A.HorizontalFlip(p=0.25),
        A.Transpose(p=0.25),
        A.RandomRotate90(p=0.25),
    ], p =1.0),
    # To address the barrel distortions and pincushion distortions
    A.OneOf([
        # Apply grid distortion with 30% of chance
        A.GridDistortion(p=0.3),
        A.OpticalDistortion(distort_limit=2,shift_limit=0.5, p=0.3),
        A.ElasticTransform(p=0.3, alpha=120, sigma=120*0.05, alpha_affine=None),
    ],p=1.0),
    A.OneOf([
        A.RandomBrightnessContrast(p=0.25),
    ], p=1.0),
])

test_augment = A.RandomCrop(height=CROP_SIZE[0], width= CROP_SIZE[1], p=1.0)
'''
Class Data Loader iterates over image data (input images and their corresponding masks), 
                                apply augmentations, 
                                and return batches of processed data for training or evaluation.
                                
    batch_size -> Number of images per batch
    resize_size -> The size of the image to be resizedc
    crop_size -> Size of the cropped region used for data augmentation
    input_img_paths -> List of paths to the input images 
    target_img_paths -> List of paths to the corresponding target segmentation masks
    data_type -> Type of the dataset ("Train" or "Test") 
'''
class DataLoader(tf.keras.utils.Sequence):
    def __init__(self, batch_size, resize_size, crop_size, input_img_paths, target_img_paths, data_type):
        self.batch_size = batch_size
        self.resize_size = resize_size
        self.crop_size = crop_size
        self.input_img_paths = input_img_paths
        self.target_img_paths = target_img_paths
        self.data_type = data_type
        self.train_transform = train_augment
        self.test_transform = test_augment

    # Total number of batches in the dataset
    def __len__(self):
        return len(self.target_img_paths)//self.batch_size

    # Method converts RGB images into a one-hot encoded format, where each pixel is represented by a binary vector
    # indicating the class it belongs to.
    def rgbToOnehot(self, rgb_mat, color_dict = COLOR_VALUES):
        # The number of unique colors (classes) in the color_dictionary
        num_classes = len(color_dict)
        # One hot encoded dimensions --> height, width, num_classes
        shape = rgb_mat.shape[:2]+(num_classes,)
        mat= np.zeros(shape, dtype=np.float32)
        for i, _ in enumerate(color_dict):
            mat[:,:,i]= np.all(rgb_mat.reshape((-1,3))==color_dict[i], axis=1).reshape(shape[:2])
        return mat

    # Applies K-means clustering to an input image in order to reduce the number of colors in the image
    # Segments the image into K clusters using K-means clustering.
    def KNNOutput(self, img):
        # Z --> (img.height*img.width, 3)
        Z = img.reshape((-1,3))
        Z = np.float32(Z)
        '''
            Stop the algorith in the following scenarios
            cv2.TERM_CRITERIA_EPS: Stop the algorithm when the specified accuracy (epsilon) is reached
            cv2.TERM_CRITERIA_MAX_ITER: Stop the algorithm after a maximum number of iterations
            (100, 1.0): The algorithm will stop either when 100 iterations are completed or when the change in cluster
                        centers is less than 1.0 
        '''
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1.0 )
        K = 2 # ---> Number of clusters
        # 10 --> number of times the algorithm will be executed using different initial cluster centers.
        _, label,center = cv2.kmeans(Z,K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]
        result = res.reshape((img.shape))
        return result

    # Loads and processes a single batch of data from the dataset, performing augmentations, one-hot encoding,
    # and K-means clustering
    def __getitem__(self, idx):
        i = idx*self.batch_size
        batch_input_img_paths = self.input_img_paths[i:i+self.batch_size]
        batch_target_img_paths = self.target_img_paths[i:i + self.batch_size]
        # x --> stores the batch of input images
        # y --> stores the batch of one-hot encoded masks
        # z --> stores the batch of K-means processed images
        x = np.zeros((self.batch_size,) + self.crop_size+ (3,), dtype="float32")
        y = np.zeros((self.batch_size,) + self.crop_size + (2,), dtype="float32")
        z = np.zeros((self.batch_size,) + self.crop_size + (3,), dtype="float32")

        for j, (input_image, input_mask) in enumerate(zip(batch_input_img_paths, batch_target_img_paths)):
            img = cv2.imread(input_image)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, self.crop_size)

            mask = cv2.imread(input_mask)
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
            mask = cv2.resize(mask, self.crop_size)

            if self.data_type == "Train":
                augment = self.train_transform(image = img, mask = mask)
            else:
                augment = self.test_transform(image = img, mask= mask)

            knn_image = self.KNNOutput(img)
            knn_image = knn_image.astype("float32")/255
            mask = self.rgbToOnehot(mask).astype('float32')
            # x[j], y[j], z[j] = img.astype('float32'), mask, knn_image
            x[j] = img.astype('float32')
            y[j] = mask
            z[j] = knn_image

            return (x,z), y

def getDataLoader(batch_size):
    input_img_paths = sorted([os.path.join(IMAGES_DIR, x) for x in os.listdir(IMAGES_DIR)])
    target_img_paths = sorted([os.path.join(MASKS_DIR, x) for x in os.listdir(MASKS_DIR)])

    print(f"Number of images: {len(input_img_paths)}")
    print(f"Number of masks: {len(target_img_paths)}")

    x_train, x_test, y_train, y_test = train_test_split(input_img_paths,
                                                        target_img_paths,
                                                        test_size= TEST_SIZE,
                                                        random_state= SEED)
    trainGen = DataLoader(batch_size=batch_size,
                          resize_size=RESIZE_SIZE,
                          crop_size=CROP_SIZE,
                          input_img_paths= x_train,
                          target_img_paths=y_train,
                          data_type="Train")

    testGen = DataLoader(
        batch_size=batch_size,
        resize_size=RESIZE_SIZE,
        crop_size=CROP_SIZE,
        input_img_paths=x_test,
        target_img_paths=y_test,
        data_type="Test"
    )

    return trainGen, testGen



