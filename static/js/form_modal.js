document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('confirmModal');
  if (modal && modal.dataset.show === '1') {
    modal.style.display = 'block';

    document.getElementById('modalHomeBtn').addEventListener('click', () => {
      window.location.href = '/experiments'; // Cambia con la tua URL di destinazione
    });
  }
});
