function showSelectedPhoto(event) {
    var file = event.target.files[0];
    var reader = new FileReader();

    reader.onload = function(e) {
        var imageElement = document.getElementById('result-image');
        imageElement.src = e.target.result;
        imageElement.style.display = 'inline';
        // Hide question mark
        document.getElementById('question-mark').style.display = 'none';
    };

    if (file) {
        reader.readAsDataURL(file);
    } else {
        alert('No file selected. Please select an image file.');
    }
};

function uploadPhoto() {
    var file = document.getElementById('photo').files[0];
    var reader = new FileReader();
    var uploadButton = document.querySelector('.form-container button');
    var uploadButtonOriginalText = uploadButton.textContent;

    var questionMark = document.getElementById('question-mark');
    var questionMarkOriginalDisplay = 'block';

    reader.onloadend = function() {
        // For local development, assuming the API is running on the same machine on port 3000
        // const apiUrl = `http://${window.location.hostname}:3000/whatispants`
        // Use your API Gateway endpoint URL here
        const apiUrl = 'https://1pt6rewihj.execute-api.eu-west-1.amazonaws.com/Prod/whatispants/'

        // Change button text to "Uploading..."
        uploadButton.textContent = "Uploading...";
        uploadButton.disabled = true;
        // Start rotating the question mark while uploading
//        questionMark.style.display = questionMarkOriginalDisplay;
//        questionMark.classList.add('rotate');

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
            var noPantsText = document.getElementById('no-pants-text');

            uploadButton.textContent = uploadButtonOriginalText;
            uploadButton.disabled = false;

            if (data.num_pants_found === 0) {
                noPantsText.style.display = 'block';
            } else {
                noPantsText.style.display = 'none';
            }

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
            // Revert button text back to "Upload Photo" in case of error
            uploadButton.textContent = uploadButtonOriginalText;
            uploadButton.disabled = false;
//            questionMark.style.display = questionMarkOriginalDisplay;
//            questionMark.classList.remove('rotate');
        });
    }
    if (file) {
        reader.readAsDataURL(file);
    } else {
        alert('No file selected. Please select an image file.');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('photo').onchange = showSelectedPhoto;
})
