document.addEventListener('DOMContentLoaded', () => {
  const approvedIssueModal = document.getElementById('approvedIssueModal');
  const closeApprovedModalBtn = document.getElementById('closeApprovedIssueModal');
  const cancelResolveBtn = document.getElementById('cancelResolveIssueBtn');
  const resolveIssueBtn = document.getElementById('resolveIssueBtn');

  // Elementi dove mostrare i dati
  const approvedTitle = document.getElementById('approved-modal-title');
  const approvedDescription = document.getElementById('approved-modal-description');
  const approvedExperiment = document.getElementById('approved-modal-experiment');
  const approvedResolved = document.getElementById('approved-modal-resolved');
  const approvedIssueIdInput = document.getElementById('approved-modal-issue-id');

  // Funzione per aprire il modal con i dati dell'issue
  function openApprovedIssueModal(issue) {
    approvedTitle.textContent = issue.title || '';
    approvedDescription.textContent = issue.description || '';
    approvedExperiment.textContent = issue.experiment || '';
    approvedResolved.textContent = issue.resolved ? "Risolto" : "Non risolto";
    approvedIssueIdInput.value = issue.id || '';

    approvedIssueModal.style.display = 'block';
  }

  // Esempio: aprire modal cliccando su una card issue approvata
  document.querySelectorAll('.card-container .user-card[data-issue-id]').forEach(card => {
    card.addEventListener('click', () => {
      const issueId = card.getAttribute('data-issue-id');

      // Qui puoi recuperare i dati dal DOM o da un API, per esempio:
      const issue = {
        id: issueId,
        title: card.querySelector('.issue-title')?.textContent || '',
        description: card.querySelector('.issue-description')?.textContent || '',
        experiment: card.querySelector('.issue-experiment')?.textContent || '',
        resolved: false // se hai un attributo, leggi da lì
      };

      openApprovedIssueModal(issue);
    });
  });

  // Chiudi modal con la X
  closeApprovedModalBtn.addEventListener('click', () => {
    approvedIssueModal.style.display = 'none';
  });

  // Chiudi modal con il bottone Annulla
  cancelResolveBtn.addEventListener('click', () => {
    approvedIssueModal.style.display = 'none';
  });

  // Gestione del click su "Segna come Risolta"
  resolveIssueBtn.addEventListener('click', () => {
    const issueId = approvedIssueIdInput.value;

    // Qui puoi fare una chiamata AJAX per aggiornare lo stato sul server
    // esempio con fetch (adatta URL e metodo a seconda del tuo backend)
    fetch(`/issues/${issueId}/resolve/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'), // funzione getCookie da definire o usare un modo per ottenere CSRF
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ resolved: true }),
    })
      .then(response => {
        if (response.ok) {
          alert('Issue segnata come risolta!');
          approvedIssueModal.style.display = 'none';
          // opzionale: aggiorna la UI per riflettere il cambio di stato
          location.reload(); // o aggiorna solo la card dinamicamente
        } else {
          alert('Errore nel segnalare come risolta.');
        }
      })
      .catch(() => {
        alert('Errore di connessione.');
      });
  });

  // Funzione per recuperare il cookie CSRF (necessaria per POST in Django)
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Chiudi modal cliccando fuori dal contenuto
  window.addEventListener('click', (event) => {
    if (event.target === approvedIssueModal) {
      approvedIssueModal.style.display = 'none';
    }
  });
});
