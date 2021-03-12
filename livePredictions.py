# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 09:55:54 2021

@author: Sayan
"""


import keras
import numpy as np
import librosa


SAVED_MODEL_PATH = 'model.h5'
class _livePredictions:
    """
    Main class of the application.
    """
    model = None
    
    _instance = None

   # def __init__(self, path, file):
    """
     Init method is used to initialize the main parameters.
     """
     #    self.path = path
    # self.file = file
    
    # def load_model(self):
    """
     Method to load the chosen model.
     :param path: path to your h5 model.
     :return: summary of the model with the .summary() function.
     """
       # self.loaded_model = keras.models.load_model(self.path)
        #how to print mreturn self.loaded_model.summary()

    def makepredictions(self,file):
        """
        Method to process the files and create your features.
        """
        data, sampling_rate = librosa.load(file)
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
        x = np.expand_dims(mfccs, axis=1)
        x = np.expand_dims(x, axis=0)
        predictions = self.model.predict(x)
        predictions = np.argmax(predictions)
        print("Prediction is", " ", self.convertclasstoemotion(predictions))
        return self.convertclasstoemotion(predictions)

    @staticmethod
    def convertclasstoemotion(pred):
        """
        Method to convert the predictions (int) into human readable strings.
        """
        
        label_conversion = {'0': 'neutral',
                            '1': 'calm',
                            '2': 'happy',
                            '3': 'sad',
                            '4': 'angry',
                            '5': 'fearful',
                            '6': 'disgust',
                            '7': 'surprised'}

        for key, value in label_conversion.items():
            if int(key) == pred:
                label = value
        return label
def livePredictions():


    # ensure an instance is created only the first time the factory function is called
    if _livePredictions._instance is None:
        _livePredictions._instance = _livePredictions()
        _livePredictions.model = keras.models.load_model(SAVED_MODEL_PATH)
        print(_livePredictions.model.summary())
    return _livePredictions._instance
    
if __name__ == "__main__":

    # create 2 instances of the keyword spotting service
    lv = livePredictions()
    lv1 = livePredictions()

    # check that different instances of the keyword spotting service point back to the same object (singleton)
    assert lv in lv1
 #   pred=lv.makepredictions(file_name)

    # make a prediction
   # keyword = kss.predict("down.wav")
    #(keyword)
