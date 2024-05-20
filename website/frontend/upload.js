function uploadPhoto() {
    var file = document.getElementById('photo').files[0];
    var reader = new FileReader();
    reader.onloadend = function() {
        // For local development, assuming the API is running on the same machine on port 3000
        // const apiUrl = `http://${window.location.hostname}:3000/whatispants`
        // Use your API Gateway endpoint URL here
        const apiUrl = 'https://1pt6rewihj.execute-api.eu-west-1.amazonaws.com/Prod/whatispants/'
        fetch(
            apiUrl,
            {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: reader.result.split(',')[1]  // Send base64 string without the prefix
            }
        )
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            var imageElement = document.getElementById('result-image')
            // Decode the base64 string and set it as the image source
            imageElement.src = 'data:image/jpeg;base64,' + data.result;
            // Show the image element once the annotated image is loaded
            // `inline` ensures it's centered horizontally.
            imageElement.style.display = 'inline';
            // Hide question mark
            document.getElementById('question-mark').style.display = 'none';
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
    if (file) {
        reader.readAsDataURL(file);
    } else {
        alert('No file selected. Please select an image file.');
    }
}
