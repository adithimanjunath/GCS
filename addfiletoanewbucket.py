from flask import Flask, render_template, request, jsonify
from google.cloud import storage

app = Flask(__name__)

# Function to list all Google Cloud Storage buckets
def list_buckets():
    try:
        # Create a storage client
        storage_client = storage.Client()
        # List all buckets and extract bucket names
        buckets = list(storage_client.list_buckets())
        bucket_names = [bucket.name for bucket in buckets]
        return bucket_names
    except Exception as e:
        return str(e)

# Route to list all buckets
@app.route('/list_buckets', methods=['GET'])
def list_buckets_route():
    try:
        # Call the list_buckets function
        buckets = list_buckets()
        return jsonify({'buckets': buckets}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Function to create a new Google Cloud Storage bucket
def create_bucket(bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    print(f'Bucket {bucket_name} created.')

# Function to upload a file to a Google Cloud Storage bucket
def upload_file(bucket_name, local_file_path, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)  # Use destination_blob_name
    blob.upload_from_filename(local_file_path)  # Use local_file_path
    print(f'File {local_file_path} uploaded to {destination_blob_name} in {bucket_name}.')

# Route to handle file upload
@app.route('/upload_file', methods=['POST'])
def upload_file_route():
    # Extract data from the JSON request
    data = request.json
    bucket_name = data['bucket_name']
    local_file_path = data['local_file_path']
    destination_blob_name = data['destination_blob_name']

    try:
        # Create the bucket
        create_bucket(bucket_name)
        # Upload the file to the bucket
        upload_file(bucket_name, local_file_path, destination_blob_name)
        return jsonify({'message': f'File uploaded successfully to bucket {bucket_name}.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Render the index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
