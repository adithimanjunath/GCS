// script.js (JavaScript code)

document.addEventListener('DOMContentLoaded', function() {
    const createBucketForm = document.getElementById('createBucketForm');
    const uploadFileForm = document.getElementById('uploadFileForm');
    const deleteFileForm = document.getElementById('deleteFileForm');
    const downloadFileForm = document.getElementById('downloadFileForm');
    const readDataForm = document.getElementById('readDataForm');
    const dataContainer = document.getElementById('dataContainer');
    const responseMessage = document.getElementById('responseMessage');

    createBucketForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/create_bucket', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            responseMessage.innerText = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
            responseMessage.innerText = 'An error occurred.';
        });
    });

    uploadFileForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/upload_file', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            responseMessage.innerText = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
            responseMessage.innerText = 'An error occurred.';
        });
    });

    deleteFileForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/delete_file', {
            method: 'POST',
            body: JSON.stringify(Object.fromEntries(formData)),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            responseMessage.innerText = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
            responseMessage.innerText = 'An error occurred.';
        });
    });

    downloadFileForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/download_file', {
            method: 'POST',
            body: JSON.stringify(Object.fromEntries(formData)),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            responseMessage.innerText = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
            responseMessage.innerText = 'An error occurred.';
        });
    });

    readDataForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/read_data', {
            method: 'POST',
            body: JSON.stringify(Object.fromEntries(formData)),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            renderData(data.data);
        })
        .catch(error => {
            console.error('Error:', error);
            responseMessage.innerText = 'An error occurred.';
        });
    });

    function renderData(data) {
        dataContainer.innerHTML = '';
        const table = document.createElement('table');
        const thead = table.createTHead();
        const tbody = table.createTBody();
        const headerRow = thead.insertRow();
        for (const item of data[0]) {
            const th = document.createElement('th');
            th.textContent = item;
            headerRow.appendChild(th);
        }
        for (let i = 1; i < data.length; i++) {
            const row = tbody.insertRow();
            for (const item of data[i]) {
                const cell = row.insertCell();
                cell.textContent = item;
            }
        }
        dataContainer.appendChild(table);
    }
});
