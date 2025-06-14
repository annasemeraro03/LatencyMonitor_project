document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('issueModal');
    const closeBtn = document.getElementById('closeIssueModal');
    const modalTitle = document.getElementById('modal-title');
    const modalDescription = document.getElementById('modal-description');
    const modalIssueId = document.getElementById('modal-issue-id');

    // Funzione per aprire modal con dati
    function openModal(issueId, title, description) {
        modalTitle.textContent = title;
        modalDescription.textContent = description;
        modalIssueId.value = issueId;
        modal.style.display = 'block';
    }

    // Chiudi modal
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Chiudi modal cliccando fuori dal contenuto
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Apri modal al click su "Vedi dettagli"
    document.querySelectorAll('.details-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const issueId = btn.getAttribute('data-issue-id');
            const card = btn.closest('.user-card');
            const title = card.querySelector('h3').textContent;
            const description = card.querySelector('p:nth-of-type(4)')?.textContent || 'Nessuna descrizione disponibile';
            
            // Se non hai la descrizione in pagina, potresti fare fetch Ajax qui per recuperarla
            openModal(issueId, title, description);
        });
    });

    // Funzione per chiamate fetch con CSRF token
    function fetchWithCSRF(url, options = {}) {
        const csrftoken = getCookie('csrftoken');
        options.headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            ...options.headers,
        };
        return fetch(url, options);
    }

    // Funzione per prendere il cookie csrf
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Controlla se cookie inizia con nome richiesto
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Bottone Approva
    document.getElementById('approveIssueBtn').addEventListener('click', () => {
        const issueId = modalIssueId.value;
        if (!issueId) return;
        fetchWithCSRF(`/issues/approve/${issueId}/`, { method: 'GET' })
            .then(res => {
                if (res.ok) {
                    alert('Issue approvata!');
                    window.location.reload(); // o aggiorna dinamicamente
                } else {
                    alert('Errore nell\'approvazione.');
                }
            });
    });

    // Bottone Rifiuta
    document.getElementById('rejectIssueBtn').addEventListener('click', () => {
        const issueId = modalIssueId.value;
        if (!issueId) return;
        fetchWithCSRF(`/issues/reject/${issueId}/`, { method: 'GET' })
            .then(res => {
                if (res.ok) {
                    alert('Issue rifiutata!');
                    window.location.reload();
                } else {
                    alert('Errore nel rifiuto.');
                }
            });
    });
});