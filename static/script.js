// script.js

document.addEventListener('DOMContentLoaded', function() {
    const fetchForm = document.getElementById('fetchForm');
    const dataDiv = document.getElementById('data');
    const errorDiv = document.getElementById('error');
    const loader = document.getElementById('loader');

    fetchForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        errorDiv.textContent = '';
        dataDiv.innerHTML = '';
        loader.style.display = 'block';

        const formData = new FormData(fetchForm);
        const bucketName = formData.get('bucketName');
        const fileName = formData.get('fileName');
        const rowNumbers = formData.get('rowNumbers');

        try {
            const response = await fetch(`/fetchData?bucketName=${bucketName}&fileName=${fileName}&rowNumbers=${rowNumbers}`);
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            const data = await response.text();
            dataDiv.innerHTML = data;
        } catch (error) {
            console.error('Error fetching data:', error);
            errorDiv.textContent = 'Error fetching data. Please try again later.';
        } finally {
            loader.style.display = 'none';
        }
    });
});
