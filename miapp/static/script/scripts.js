document.addEventListener('DOMContentLoaded', function () {
    const notificationsButton = document.getElementById('notifications');
    const dropdown = document.getElementById('dropdown');

    notificationsButton.addEventListener('click', function () {
        if (dropdown.style.display === 'none' || dropdown.style.display === '') {
            dropdown.style.display = 'block';
        } else {
            dropdown.style.display = 'none';
        }
    });

    // Cierra el dropdown si se hace clic fuera de él
    document.addEventListener('click', function (event) {
        if (!notificationsButton.contains(event.target) && !dropdown.contains(event.target)) {
            dropdown.style.display = 'none';
        }
    });
});
