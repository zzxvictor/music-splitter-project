function upload(event) {
    console.warn("It's taking awhile....");
}

const form = document.getElementById('uploader');
form.addEventListener('submit', upload);
