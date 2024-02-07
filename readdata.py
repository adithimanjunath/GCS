from flask import Flask, render_template, request
from google.cloud import storage
import csv

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get bucket name and blob name from the form
        bucket_name = request.form['bucket_name']
        blob_name = request.form['blob_name']
        # Read data from Google Cloud Storage
        data = read_data_from_gcs(bucket_name, blob_name)
        return render_template('readdata.html', data=data)
    else:
        return render_template('readdata.html')

if __name__ == "__main__":
    app.run(debug=True)
