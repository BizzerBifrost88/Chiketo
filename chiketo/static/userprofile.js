document.addEventListener('DOMContentLoaded', function () {
    const profileImage = document.getElementById('profileImage');
    const profileDropdown = document.getElementById('profileDropdown');
    const closeDropdown = document.getElementById('closeDropdown');

    profileImage.addEventListener('click', () => {
        profileDropdown.style.display = profileDropdown.style.display === 'block' ? 'none' : 'block';
    });

    closeDropdown.addEventListener('click', () => {
        profileDropdown.style.display = 'none';
    });
});
     