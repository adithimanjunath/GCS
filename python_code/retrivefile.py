from flask import Flask, render_template, request, jsonify
from google.cloud import storage
import os

app = Flask(__name__)

def download_file(bucket_name, blob_name, local_file_path):
    """Downloads a file from Google Cloud Storage and stores it locally."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.download_to_filename(local_file_path)
        print(f'File downloaded from GCS and stored locally at: {local_file_path}')
        return True
    except Exception as e:
        print(f'Error downloading file: {e}')
        return False

@app.route('/')
def index():
    return render_template('retrivefile.html')

@app.route('/download_file', methods=['POST'])
def download_file_route():
    data = request.json
    bucket_name = data['bucket_name']
    blob_name = data['blob_name']
    local_file_path = data['local_file_path']

    try:
        if download_file(bucket_name, blob_name, local_file_path):
            return jsonify({'message': f'File downloaded successfully to {local_file_path}'}), 200
        else:
            return jsonify({'error': 'Failed to download file'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
