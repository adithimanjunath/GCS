# app.py (Flask backend)

from flask import Flask, render_template, request, jsonify
from google.cloud import storage
import os
import csv

app = Flask(__name__)

def create_bucket(bucket_name):
    """Creates a new Google Cloud Storage bucket."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.create_bucket(bucket_name)
        return True, f'Bucket {bucket_name} created successfully.'
    except Exception as e:
        return False, str(e)

def upload_file(bucket_name, file):
    """Uploads a file to Google Cloud Storage."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
        return True
    except Exception as e:
        return False

def delete_file(bucket_name, file_name):
    """Deletes a file from a Google Cloud Storage bucket."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.delete()
        return True, f'File {file_name} deleted from {bucket_name}.'
    except Exception as e:
        return False, str(e)

def download_file(bucket_name, blob_name, local_file_path):
    """Downloads a file from Google Cloud Storage and stores it locally."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.download_to_filename(local_file_path)
        return True, f'File downloaded from GCS and stored locally at: {local_file_path}'
    except Exception as e:
        return False, str(e)

def read_data_from_gcs(bucket_name, blob_name):
    """Reads data from a CSV file in Google Cloud Storage."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        data = blob.download_as_string().decode('utf-8')
        csv_data = csv.reader(data.splitlines())
        return list(csv_data)
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('app.html')

@app.route('/create_bucket', methods=['POST'])
def create_bucket_route():
    try:
        bucket_name = request.form['bucket_name']
        if not bucket_name:
            return jsonify({'error': 'Bucket name is required.'}), 400

        success, message = create_bucket(bucket_name)
        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_file', methods=['POST'])
def upload_file_route():
    try:
        bucket_name = request.form['bucket_name']
        file = request.files['file']
        
        if not bucket_name or not file:
            return jsonify({'error': 'Bucket name and file are required.'}), 400

        if upload_file(bucket_name, file):
            return jsonify({'message': f'File {file.filename} uploaded successfully to bucket {bucket_name}.'}), 200
        else:
            return jsonify({'error': 'Failed to upload file.'}), 500
    except Exception as e:
        print(f"Error uploading file: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/delete_file', methods=['POST'])
def delete_file_route():
    try:
        bucket_name = request.form['bucket_name']
        file_name = request.form['file_name']
        
        if not bucket_name or not file_name:
            return jsonify({'error': 'Bucket name and file name are required.'}), 400

        success, message = delete_file(bucket_name, file_name)
        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_file', methods=['POST'])
def download_file_route():
    try:
        bucket_name = request.form['bucket_name']
        blob_name = request.form['blob_name']
        local_file_path = request.form['local_file_path']
        
        if not bucket_name or not blob_name or not local_file_path:
            return jsonify({'error': 'Bucket name, blob name, and local file path are required.'}), 400

        success, message = download_file(bucket_name, blob_name, local_file_path)
        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/read_data', methods=['POST'])
def read_data_route():
    try:
        bucket_name = request.form['bucket_name']
        blob_name = request.form['blob_name']
        
        if not bucket_name or not blob_name:
            return jsonify({'error': 'Bucket name and blob name are required.'}), 400

        data = read_data_from_gcs(bucket_name, blob_name)
        return jsonify({'data': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
