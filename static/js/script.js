document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    var fileInput = document.getElementById('fileInput');
    var loadingBar = document.getElementById('loadingBar');
    var resultDiv = document.getElementById('result');

    // Reset loading bar and clear any previous errors
    loadingBar.style.width = '0%';
    loadingBar.textContent = '0%';
    resultDiv.textContent = ''; // Clear any previous messages or errors

    if (!fileInput.files.length) {
        resultDiv.textContent = 'Please select a file before submitting.';
        return;
    }

    var formData = new FormData();
    formData.append('file', fileInput.files[0]);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/', true);

    xhr.upload.addEventListener('progress', function(e) {
        if (e.lengthComputable) {
            var percentComplete = (e.loaded / e.total) * 100;
            loadingBar.style.width = percentComplete + '%';
            loadingBar.textContent = Math.round(percentComplete) + '%';
        }
    });

    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.status === 'success') {
                var link = document.createElement('a');
                link.href = response.download_url;
                link.download = response.filename;
                link.textContent = 'Download MP3';
                link.className = 'download-link'; // Add the download-link class here
                resultDiv.innerHTML = '';
                resultDiv.appendChild(link);
            } else {
                resultDiv.textContent = response.message;
            }
        } else {
            // Display an error message if the server returns a failure response
            resultDiv.textContent = 'An error occurred during the conversion. Please try again.';
        }
    };

    xhr.onerror = function() {
        // Handle network errors
        resultDiv.textContent = 'A network error occurred. Please check your connection and try again.';
    };

    xhr.responseType = 'text'; // Expect a text response that will be JSON-parsed
    xhr.send(formData);
});

document.getElementById('fileInput').addEventListener('change', function() {
    var loadingBar = document.getElementById('loadingBar');
    var resultDiv = document.getElementById('result');

    // Reset the loading bar and clear error messages when a new file is selected
    loadingBar.style.width = '0%';
    loadingBar.textContent = '0%';
    resultDiv.textContent = ''; // Clear previous messages or errors
});
