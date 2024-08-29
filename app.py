import os
from flask import Flask, request, jsonify, send_from_directory, render_template
from moviepy.editor import VideoFileClip
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads/input')
OUTPUT_FOLDER = os.path.join(os.getcwd(), 'uploads/output')
ALLOWED_EXTENSIONS = {'mp4'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Helper function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the file part is present
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file part in the request'}), 400

        file = request.files['file']

        # If user does not select a file, the browser submits an empty part without filename
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_filepath)

            try:
                # Convert MP4 to MP3
                clip = VideoFileClip(input_filepath)
                output_filename = f"{uuid.uuid4().hex}.mp3"
                output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                clip.audio.write_audiofile(output_filepath)
                clip.close()

                return jsonify({
                    'status': 'success',
                    'download_url': f'/download/{output_filename}',
                    'filename': output_filename
                })

            except Exception as e:
                return jsonify({'status': 'error', 'message': f'Failed to convert video: {str(e)}'}), 500

        return jsonify({'status': 'error', 'message': 'File type not allowed'}), 400

    return render_template('index.html')

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(debug=True)
