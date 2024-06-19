# 🗂 FREEDROP - file exchanger
# ✅ Fully free
# ✅ 10MB File and no limits
# ✅ Direct link
# 🔑 Open source
# 🐍 Works on python
# 📂 Tokens for download file

#Vesrion: 1.0.1
#Changelog:
# - Patch 
#   - Deletes filename in direct link
#Author: github.com/nikitapro225
#TG: t.me/cho_ghg

from flask import Flask, request, send_from_directory, jsonify, render_template
import os
import uuid
url = '127.0.0.1' #Set your url

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # Limit to upload 10MB
UPLOAD_FOLDER = 'uploads' #Folder for save
os.makedirs(UPLOAD_FOLDER, exist_ok=True) #Create UPLOAD_FOLDER

@app.errorhandler(413) #On large file
def request_entity_too_large(error):
    return 'File too large. Maximum allowed file size is 10 MB.', 413

@app.route('/', methods=['GET', 'POST']) #Main
def upload_file():
    if request.method == 'POST' and 'file' in request.files: #Submit
        file = request.files['file']
        if file.filename == '': #No selected file
            return 'No selected file', 400
        for i in list('\\/*?:"<>|'): #Invalid filename
            if i in file.filename:
                return 'Invalid filename', 400

        
        token = str(uuid.uuid4()) # Generate a unique token for the file
        file_type = os.path.splitext(file.filename)[1]
        file_path = os.path.join(UPLOAD_FOLDER, token, file.filename)
        os.makedirs(os.path.join(UPLOAD_FOLDER, token), exist_ok=True)
        # Saves file
        file.save(file_path)
        file_url = f'https://{url}/{token}/{file.filename}'
        return jsonify({'token': token, 'file': file.filename, 'url': file_url})
    return render_template('index.html')

@app.route('/bg.png', methods=['GET', 'POST']) #Background
def bg():
    return open('bg.png', 'rb').read()

@app.route('/<token>') #Download
def get_file_info(token, filename):
    file_dir = os.path.join(UPLOAD_FOLDER, token)
    if os.path.isdir(file_dir):
        files = os.listdir(file_dir) #Files in folder
        if files:
            file_name = files[0] #File
            return send_from_directory(file_dir + '\\', filename) #Send file
            else:
                return 'File not found', 404
        else:
            return 'No files found in this directory', 404
    else:
        return 'Directory not found', 404

if __name__ == '__main__':
    app.run() #Run app
