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

def fetch_row(data, row_index):
    """Fetches one entire row from the data based on the row index."""
    if 0 <= row_index < len(data):
        return data[row_index]
    else:
        return "Invalid row index"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get bucket name, blob name, and row index from the form
        bucket_name = request.form['bucket_name']
        blob_name = request.form['blob_name']
        row_index = int(request.form['row_index'])  # Convert to integer
        # Read data from Google Cloud Storage
        data = read_data_from_gcs(bucket_name, blob_name)
        # Fetch the requested row
        row_data = fetch_row(data, row_index)
        return render_template('readselectedline.html', data=row_data)
    else:
        return render_template('readselectedline.html')

if __name__ == "__main__":
    app.run(debug=True)
