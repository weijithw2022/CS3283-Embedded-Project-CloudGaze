import tensorflow as tf
from dataloader import *
from network import *
from loss import *
from config import *
from utils import *
import logging
import os

def main():
    logger = logging.getLogger(__name__)

    logger.info("[Info] Getting DataLoader")
    trainGen, testGen = getDataLoader(batch_size=BATCH_SIZE)

    logger.info("[Info] Creating Network")
    model = getModel()

    logger.info('[Info] Summary of model \n')
    logger.info(model.summary())

    model.compile(optimizer=tf.keras.optimizers.Adam(INITIAL_LEARNING_RATE),
                  loss=bceDiceLoss, metrics=[diceCoef])
    '''
        ModelCheckpoint:
            Monitors the validation Dice coefficient (val_diceCoef)
            Saves the model's weights only when the validation Dice coefficient improves (save_best_only=True).
            Model is saved to the directory weights
        ReduceLROnPlateau(Reduce Learning Rate on Plateau):
            Reduces the learning rate by a factor of 0.1 if the validation Dice coefficient plateaus for 20 epochs
            Sets a minimum learning rate (min_lr=0.00001) to prevent the learning rate from becoming too small.
    '''
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(os.path.join(WEIGHTS_DIR, 'Best.keras'),
                                           monitor='val_diceCoef',
                                           mode="max",
                                           verbose=1,
                                           save_best_only=True,
                                           save_weights_only=False),
        tf.keras.callbacks.ReduceLROnPlateau(monitor='val_diceCoef',
                                             mode="max",
                                             factor=0.1,
                                             patience=20,
                                             min_lr=0.00001)
    ]
    # Use the predefined callbacks to save the best model and adjust the learning rate during training
    model.fit(trainGen, validation_data=testGen, epochs=EPOCHS, verbose=1, callbacks=callbacks)
    logger.info("[Info] Training Finished")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename=os.path.join(LOG_DIR, 'app.log'),
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filemode='w')

    sys.stdout = LoggerWriter(logging.info)
    sys.stderr = LoggerWriter(logging.error)

    main()