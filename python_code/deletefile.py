from flask import Flask, render_template, request, jsonify
from google.cloud import storage

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('deletefile.html')

@app.route('/delete_file', methods=['POST'])
def delete_file():
    data = request.json
    bucket_name = data['bucket_name']
    file_name = data['file_name']

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)

    blob.delete()

    return jsonify({'message': f'File {file_name} deleted from {bucket_name}.'})

if __name__ == '__main__':
    app.run(debug=True)
