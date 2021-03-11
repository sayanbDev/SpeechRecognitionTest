import keras
import numpy as np
import librosa
from flask import Flask,request,jsonify,render_template,redirect

import random
import os
from pydub import AudioSegment



app = Flask(__name__)
app.config["MAX_IMAGE_FILESIZE"] = 26214400
app.config["ALLOWED_FILE_EXTENSIONS"] = ["MP3", "WAV", "AAC"]


class livePredictions:
    """
    Main class of the application.
    """

    def __init__(self, path, file):
        """
        Init method is used to initialize the main parameters.
        """
        self.path = path
        self.file = file

    def load_model(self):
        """
        Method to load the chosen model.
        :param path: path to your h5 model.
        :return: summary of the model with the .summary() function.
        """
        self.loaded_model = keras.models.load_model(self.path)
        return self.loaded_model.summary()

    def makepredictions(self):
        """
        Method to process the files and create your features.
        """
        data, sampling_rate = librosa.load(self.file)
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
        x = np.expand_dims(mfccs, axis=1)
        x = np.expand_dims(x, axis=0)
        predictions = self.loaded_model.predict_classes(x)
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



def allowed_audio_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False
    
def allowed_audio(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_FILE_EXTENSIONS"]:
        return True
    else:
        return False
    

@app.route('/')
def home():
    pred = livePredictions(path='model.h5',file='a.wav')

    pred.load_model()
    play=pred.makepredictions()
    return jsonify({
                    "tweets":play})

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == "POST":
        if request.files:
            #if "filesize" in request.cookies:

               # if not allowed_audio_filesize(request.cookies["filesize"]):
                 #   print("Filesize exceeded maximum limit")
                  #  return jsonify("error", "Filesize exceeded maximum limit")
                audio_file = request.files["audio"]
                if audio_file.filename == "":
                    print("No filename")
                    return jsonify("error", "No filename")
                if allowed_audio(audio_file.filename):
                    
                    ext=audio_file.filename
                    
                    ext = ext.rsplit(".", 1)[1]
                    file_name=audio_file
                    #ismp3=false;
                 #   isaac=false;
                 
                 
                    if ext.upper()=="MP3":
                        

# os.path.exists(src)
                        dst = "converted.wav"
                        # open(src)
                        
                        sound = AudioSegment.from_mp3(audio_file)
                        sound.export(audio_file, format='wav')
                        file_name=audio_file
                        
                        #audio_file=dst
                    if ext.upper()=="AAC":
                        

# os.path.exists(src)
                        dst = "converted.wav"
                        # open(src)
                        
                        sound = AudioSegment.from_file(audio_file, "aac")
                        sound.export(audio_file, format='wav')
                        file_name=audio_file
                        
                        
                    
                   # file_name = str(random.randint(0, 100000))
                   # audio_file.save(file_name)
            
                    pred = livePredictions(path='model.h5',file=file_name)
        
                    pred.load_model()

	# instantiate keyword spotting service singleton and get prediction
   # kss = Keyword_Spotting_Service()
                    predicted_keyword = pred.makepredictions()

	# we don't need the audio file any more - let's delete it!
                    #os.remove(file_name)

	# send back result as a json file
                    result = {"keyword": predicted_keyword}
                    result["S"]="s"
                    return jsonify(result)
                else:
                    jsonify("error", "That file extension is not allowed")
                    
            
        
    
    
    
    return render_template('upload.html')

@app.route('/predict')
def predict():
    audio_file = request.files["file"]
    file_name = str(random.randint(0, 100000))
    audio_file.save(file_name)
    
    pred = livePredictions(path='model.h5',file=file_name)

    pred.load_model()

	# instantiate keyword spotting service singleton and get prediction
   # kss = Keyword_Spotting_Service()
    predicted_keyword = pred.makepredictions()

	# we don't need the audio file any more - let's delete it!
    os.remove(file_name)

	# send back result as a json file
    result = {"keyword": predicted_keyword}
    return jsonify(result)

   
            
    
    

if __name__ == "__main__":
    app.run(debug=True)
