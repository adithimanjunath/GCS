import datetime
from flask import Flask, request, render_template

app = Flask(__name__)

# Import necessary libraries
from google.cloud import storage
import csv

@app.route('/')
def index():
    return render_template('index1.html')
    
@app.route('/fetchData', methods=['GET'])
def fetch_data_from_storage():
    bucket_name = request.args.get('bucketName')
    file_name = request.args.get('fileName')
    row_numbers = request.args.get('rowNumbers')
    
    try:
        if row_numbers is None:
            return "Error: Row numbers not provided."

        # Capture the timestamp before fetching the data
        start_time = datetime.datetime.now()

        # Configure Google Cloud Storage client
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        
        # Get the blob (file) from the bucket
        blob = bucket.get_blob(file_name)
        
        if blob is None:
            return f"File '{file_name}' not found in the bucket '{bucket_name}'."

        # Download the blob's content as bytes
        data = blob.download_as_string()
        
        # Decode bytes to string and split into lines
        data_str = data.decode('utf-8')
        rows = data_str.split('\n')
        
        # Parse CSV rows
        csv_rows = csv.reader(rows)
        
        # Filter rows based on user-defined row numbers
        selected_rows = []
        for i, row in enumerate(csv_rows, start=1):
            if str(i) in row_numbers.split(','):
                selected_rows.append(', '.join(row))
        
        # Generate HTML to display selected rows
        rows_html = '<h1>Data from Google Cloud Storage:</h1>'
        for row in selected_rows:
            rows_html += f'<p>{row}</p>'
            
        # Capture the timestamp after fetching the data
        end_time = datetime.datetime.now()
        
        # Calculate the time difference
        time_difference = end_time - start_time

        # Generate HTML to display time information
        time_info_html = f"<p>Time taken to fetch data: {time_difference.total_seconds()} seconds</p>"
        time_info_html += f"<p>Time when data was fetched: {start_time}</p>"
        time_info_html += f"<p>Time when data was displayed: {end_time}</p>"

        return rows_html + time_info_html
    
    except Exception as e:
        return f"Error: {str(e)}"
    
if __name__ == '__main__':
    app.run(debug=True)
