document.addEventListener('DOMContentLoaded', () => {
    document.body.style.overflow = 'hidden'; // blocca scroll

    const modal = document.getElementById('confirmModal');
    const shouldShow = modal?.dataset.show === '1';

    if (shouldShow) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden'; // blocca scroll
    }

    const homeBtn = document.getElementById('modalHomeBtn');
    if (homeBtn) {
        homeBtn.addEventListener('click', () => {
        window.location.href = '/'; // Cambia se la tua home ha un URL diverso
        });
    }
});
