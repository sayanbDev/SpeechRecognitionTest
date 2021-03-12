
from flask import Flask,request,jsonify,render_template

from pydub import AudioSegment

from livePredictions import livePredictions



app = Flask(__name__)
app.config["MAX_IMAGE_FILESIZE"] = 26214400
app.config["ALLOWED_FILE_EXTENSIONS"] = ["MP3", "WAV", "AAC"]

SAVED_MODEL_PATH = 'model.h5'



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
    
    return jsonify({
                    "move to -> ":"/upload"})

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
                        #dst = "converted.wav"
                        # open(src)
                        
                        sound = AudioSegment.from_file(audio_file, "aac")
                        sound.export(audio_file, format='wav')
                        file_name=audio_file
                        
                        
                    
                   # file_name = str(random.randint(0, 100000))
                   # audio_file.save(file_name)
                   
                    
                    lv = livePredictions()
                    
                   
                   # pred = livePredictions(path='model.h5',file=file_name)
        
            

	# instantiate keyword spotting service singleton and get prediction
   # kss = Keyword_Spotting_Service()
                    predicted_keyword = lv.makepredictions(file_name)

	# we don't need the audio file any more - let's delete it!
                    #os.remove(file_name)

	# send back result as a json file
                    result = {"Emotion": predicted_keyword}
                    result["error"]="None"
                    return jsonify(result)
                else:
                    jsonify("error", "That file extension is not allowed")
                    
            
        
    
    
    
    return render_template('upload.html')


   
            
    
    

if __name__ == "__main__":
    app.run(debug=True)
