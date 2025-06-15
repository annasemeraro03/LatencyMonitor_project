document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('userModal');
  const closeBtn = document.getElementById('closeModal');
  const detailsBtns = document.querySelectorAll('.details-btn');

  const usernameEl = document.getElementById('modal-username');
  const emailEl = document.getElementById('modal-email');
  const userIdInput = document.getElementById('modal-user-id');

  detailsBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const userId = btn.dataset.userId;

      fetch(`/admin/user_details/${userId}/`)
        .then(res => {
          if (!res.ok) throw new Error("Errore nel caricamento dati");
          return res.json();
        })
        .then(data => {
          usernameEl.textContent = data.username;
          emailEl.textContent = `Email: ${data.email}`;
          userIdInput.value = data.id;
          modal.style.display = 'block';
        })
        .catch(err => {
          usernameEl.textContent = '';
          emailEl.textContent = 'Errore nel caricamento dei dati';
          userIdInput.value = '';
          modal.style.display = 'block';
          console.error(err);
        });
    });
  });

  closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  window.addEventListener('click', e => {
    if (e.target === modal) {
      modal.style.display = 'none';
    }
  });

  const approveBtn = document.getElementById('approveBtn');
  const rejectBtn = document.getElementById('rejectBtn');

  approveBtn.addEventListener('click', () => {
    const userId = userIdInput.value;
    console.log("Approvo utente ID:", userId);
    
    // Esempio: fai fetch per approvare (POST)
    fetch('/admin/users_approval/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'), // funzione per CSRF (vedi sotto)
      },
      body: JSON.stringify({user_id: userId, action: 'approve'})
    })
    .then(res => {
      if (res.ok) {
        alert("Utente approvato!");
        modal.style.display = 'none';
        location.reload(); // ricarica pagina per aggiornare lista
      } else {
        alert("Errore nell'approvazione");
      }
    })
    .catch(err => alert("Errore rete: " + err));
  });

  rejectBtn.addEventListener('click', () => {
    const userId = userIdInput.value;
    console.log("Rifiuto utente ID:", userId);

    fetch('/admin/users_approval/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({user_id: userId, action: 'reject'})
    })
    .then(res => {
      if (res.ok) {
        alert("Utente rifiutato!");
        modal.style.display = 'none';
        location.reload();
      } else {
        alert("Errore nel rifiuto");
      }
    })
    .catch(err => alert("Errore rete: " + err));
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Se il cookie inizia con il nome richiesto
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
