ClassicEditor
    .create(document.querySelector('#id_content'), {
        toolbar: ['bold', 'italic', 'link', 'image'],
    })
    .catch(error => {
        console.error(error);
    });
