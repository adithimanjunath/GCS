from flask import Flask, render_template, request, jsonify
from google.cloud import storage

app = Flask(__name__)

def list_buckets():
    """List all Google Cloud Storage buckets."""
    try:
        storage_client = storage.Client()
        buckets = list(storage_client.list_buckets())
        bucket_names = [bucket.name for bucket in buckets]
        return bucket_names
    except Exception as e:
        return str(e)
@app.route('/list_buckets', methods=['GET'])
def list_buckets_route():
    try:
        buckets = list_buckets()
        return jsonify({'buckets': buckets}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_bucket(bucket_name):
    """Creates a new Google Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    print(f'Bucket {bucket_name} created.')

def upload_file(bucket_name, local_file_path, destination_blob_name):
    """Uploads a file to a Google Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob("newfile.txt")
    blob.upload_from_filename("/Users/adithimshrouthy/Downloads/abc.txt")
    print(f'File {local_file_path} uploaded to {destination_blob_name} in {bucket_name}.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_file', methods=['POST'])
def upload_file_route():
    data = request.json
    bucket_name = data['bucket_name']
    local_file_path = data['local_file_path']
    destination_blob_name = data['destination_blob_name']

    try:
        create_bucket(bucket_name)
        upload_file(bucket_name, local_file_path, destination_blob_name)
        return jsonify({'message': f'File uploaded successfully to bucket {bucket_name}.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


if __name__ == "__main__":
    app.run(debug=True)
