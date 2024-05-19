function uploadPhoto() {
    var file = document.getElementById('photo').files[0];
    var reader = new FileReader();
    reader.onloadend = function() {
        fetch(
            'http://127.0.0.1:3000/whatispants',  // Use your API Gateway endpoint URL here
            {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: reader.result.split(',')[1]  // Send base64 string without the prefix
            }
        )
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Decode the base64 string and set it as the image source
            document.getElementById('resultImage').src = 'data:image/jpeg;base64,' + data.result;
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
