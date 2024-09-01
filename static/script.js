document.getElementById('downloadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var url = document.getElementById('url').value;

    if (!url) {
        document.getElementById('message').innerText = 'Please enter a URL!';
        return;
    }

    fetch('/download', {
        method: 'POST',
        body: new URLSearchParams({ 'url': url }),
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    .then(response => {
        if (response.ok) {
            // If the response is a file, force download using the blob response
            return response.blob();
        } else {
            return response.json(); // If it's not a file, it must be JSON
        }
    })
    .then(data => {
        if (data instanceof Blob) {
            // This is a file download, create a download link
            var url = window.URL.createObjectURL(data);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'video.mp4';  // or use the actual filename if available
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
            document.getElementById('message').innerText = 'Video downloaded successfully!';
            document.getElementById('message').style.color='green';
        } else {
            // This is JSON with error info
            document.getElementById('message').innerText = data.message;

        }
    })
    .catch(error => {
        console.error('Error during fetch operation:', error);
        document.getElementById('message').innerText = 'Failed to download video. Please check the URL and try again.';
    });
});
