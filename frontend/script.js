
function handle_upload(event) {
    // event.preventDefault();
    const formData = new FormData(event.target);
    const apigClient = apigClientFactory.newClient();

    apigClient.uploadPost({},
        {"email": formData.get("email"), "type": formData.get('file').type})
        .then(function (response) {
            upload_file_to_s3(response, formData)
        })
        .catch(function (error) {
            console.log("Error", error)
        });

    alert("File uploaded! We'll email you when the job is done.");
    

}

function upload_file_to_s3(event, formData) {
    const url = event['data']['presigned_url'];
    const file = formData.get('file');

    const http = new XMLHttpRequest();
    http.open('PUT', url, false);
    http.setRequestHeader('Content-type', file.type);
    http.send(file);
}

function handle_download(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const apigClient = apigClientFactory.newClient();

    apigClient.downloadFileidGet({"fileid": formData.get("file_id")})
        .then(function (response) {
            download_file_from_s3(response, formData)
        })
        .catch(function (error) {
            console.log("Error", error)
        });
}

function download_file_from_s3(event, formData) {
    const http = new XMLHttpRequest();
    http.open('GET', event['data']['presigned_url'], false);
    http.send();
    alert("File downloaded");
}


const upload = document.getElementById('uploader');
upload.addEventListener('submit', handle_upload);


const download = document.getElementById('downloader');
download.addEventListener('submit', handle_download);


