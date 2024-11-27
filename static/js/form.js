document.addEventListener('DOMContentLoaded', function () {
    function handleFormSubmit(event) {
        event.preventDefault(); 
        const form = event.target; 
        const formData = new FormData(form);
        const url = form.getAttribute('action'); 

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value, 
            }
        })
        .then(response => response.json()) 
        .then(data => {
            if (data.status === 'success') {
                alert(data.message); 
                form.reset();
            } else if (data.status === 'error') {
                const errorMessages = JSON.parse(data.message);
                let errorText = '';
                for (const field in errorMessages) {
                    errorText += `${errorMessages[field][0]}\n`;
                }
                alert(errorText); 
            }
        })
        .catch(error => console.error('Error:', error)); 
    }

    document.querySelectorAll('.subscribe-form').forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });

    document.querySelectorAll('.contact-form').forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
    document.querySelectorAll('.login-form').forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
});
