function uploadPhoto() {
    var file = document.getElementById('photo').files[0];
    var reader = new FileReader();
    reader.onloadend = function() {
        fetch(
            // 'http://127.0.0.1:3000/whatispants',
            ' https://1pt6rewihj.execute-api.eu-west-1.amazonaws.com/Prod/whatispants/',  // Use your API Gateway endpoint URL here
            {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: reader.result.split(',')[1]  // Send base64 string without the prefix
            }
        )
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            var imageElement = document.getElementById('resultImage')
            // Decode the base64 string and set it as the image source
            imageElement.src = 'data:image/jpeg;base64,' + data.result;
            // Show the image element once the annotated image is loaded
            imageElement.style.display = 'block';
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
