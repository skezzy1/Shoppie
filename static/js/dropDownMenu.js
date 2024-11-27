document.getElementById('userProfileMenu').addEventListener('click', function(event) {
    const dropdownMenu = document.getElementById('dropdownMenu');
    if (dropdownMenu.style.display === 'block') {
        dropdownMenu.style.display = 'none';
    } else {
        dropdownMenu.style.display = 'block';
    }
    document.addEventListener('click', function(e) {
        if (!dropdownMenu.contains(e.target) && !document.getElementById('userProfileMenu').contains(e.target)) {
            dropdownMenu.style.display = 'none';
        }
    });
});
