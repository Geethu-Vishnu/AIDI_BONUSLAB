from flask import Flask, request, render_template, redirect, url_for
import os
import subprocess

app = Flask(__name__)

# Set the path for the upload folder
current_directory = os.path.abspath(os.path.dirname(__file__))
upload_folder = os.path.join(current_directory, 'uploaded_files')
os.makedirs(upload_folder, exist_ok=True)
app.config['UPLOAD_FOLDER'] = upload_folder

# Function to process and execute the Python file
def process_file(file_path):
    if file_path.endswith('.py'):
        result = subprocess.run(['python', file_path], capture_output=True, text=True)
        return result.stdout
    else:
        return 'The uploaded file is not a Python file.'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        # Call your function to process the file here
        # process_file(file_path)s
        output = process_file(file_path)
        return f'File {file.filename} uploaded successfully. Output:\n{output}'
        #return f'File {file.filename} uploaded successfully'

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
