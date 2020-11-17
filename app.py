
import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
from email.message import EmailMessage
import sys
import tempfile
import mimetypes
import webbrowser

# Import the email modules we'll need
from email import policy
from email.parser import BytesParser


app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.msg']
app.config['UPLOAD_PATH'] = 'uploads'
message={
        'name':'test'
    }
my_file = ''



@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files, message=message)


@app.route('/', methods=['GET', 'POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    
    
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] :
            return "Invalid file", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

                
        with open(os.path.join(app.config['UPLOAD_PATH'], filename), 'rb') as fp:
            msg = BytesParser(policy=policy.default).parse(fp)
            message['name']=filename
            message['to']=msg['to']
            message['from']=msg['from']
            message['subject']=msg['subject']
            message['date']=msg['date']
            message['message-id']=msg['message-id']
        print('To:', message['to'])
        print('From:', message['from'])
        print('Subject:', message['subject'])
        print('Date:', message['date'])
        print(message['message-id'])  

        my_file = filename
        
 
    return render_template('index.html'), 204


@app.route('/<filename>')
def msg_parser(filename):   

    return render_template('index.html', message=message)

# @app.route('/uploads/<filename>')
# def upload(filename):
#     return send_from_directory(app.config['UPLOAD_PATH'], filename)