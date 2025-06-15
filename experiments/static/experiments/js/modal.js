document.addEventListener('DOMContentLoaded', () => {
  // Gestione modal conferma creazione
  const confirmModal = document.getElementById('confirmModal');
  if (confirmModal && confirmModal.dataset.show === '1') {
    confirmModal.style.display = 'block';
  }

  // Gestione pulsanti modali
  document.querySelectorAll('.modal-content button').forEach(btn => {
    btn.addEventListener('click', () => {
      window.location.href = '/experiments/'; // Usa la stessa URL per entrambi i modali
    });
  });
});