document.addEventListener('DOMContentLoaded', function() {
    const photodiodoCtx = document.getElementById('photodiodoChart');
    const latenzaCtx = document.getElementById('latenzaChart');
    const statusPhotodiodo = document.getElementById('status-photodiodo');
    const statusLatenza = document.getElementById('status-latenza');
    const MAX_POINTS = 40;
    let currentDevice = null;
    
    if (!photodiodoCtx || !latenzaCtx) return;

    // Funzione per estrarre il nome del dispositivo dal topic
    function getDeviceName(topic) {
        if (!topic) return null;
        const parts = topic.split('/');
        return parts.length > 1 ? parts[1] : null;
    }

    // Inizializza grafico fotodiodo
    const photodiodoChart = new Chart(photodiodoCtx.getContext('2d'), {
        type: 'line',
        data: {
            datasets: [{
                label: 'Valore Fotodiodo',
                data: [],
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 2,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'second',
                        tooltipFormat: 'HH:mm:ss'
                    }
                },
                y: {
                    beginAtZero: false
                }
            }
        }
    });

    // Inizializza grafico latenza
    const latenzaChart = new Chart(latenzaCtx.getContext('2d'), {
        type: 'line',
        data: {
            datasets: [{
                label: 'Latenza (µs)',
                data: [],
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 2,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'second',
                        tooltipFormat: 'HH:mm:ss'
                    }
                },
                y: {
                    beginAtZero: false
                }
            }
        }
    });

    // Aggiorna la vista
    function updateView() {
        const hasPhotodiodoData = photodiodoChart.data.datasets[0].data.length > 0;
        const hasLatenzaData = latenzaChart.data.datasets[0].data.length > 0;
        
        if (hasPhotodiodoData && currentDevice) {
            statusPhotodiodo.innerHTML = `
                <i class="uil uil-check-circle mr-2 text-green-500"></i>
                <span class="text-green-700">${currentDevice}</span>
            `;
        } else {
            statusPhotodiodo.innerHTML = `
                <i class="uil uil-exclamation-circle mr-2"></i>
                <span>Nessun dato disponibile</span>
            `;
        }
        
        if (hasLatenzaData && currentDevice) {
            statusLatenza.innerHTML = `
                <i class="uil uil-check-circle mr-2 text-green-500"></i>
                <span class="text-green-700">${currentDevice}</span>
            `;
        } else {
            statusLatenza.innerHTML = `
                <i class="uil uil-exclamation-circle mr-2"></i>
                <span>Nessun dato disponibile</span>
            `;
        }
    }

    // Processa i nuovi dati
    function processData(newData) {
        if (!newData || newData.length === 0) {
            updateView();
            return;
        }

        // Estrai il nome del dispositivo dal primo dato
        if (!currentDevice && newData[0].topic) {
            currentDevice = getDeviceName(newData[0].topic);
        }

        const newPhotodiodoPoints = [];
        const newLatenzaPoints = [];

        newData.forEach(item => {
            const [photodiodo, latenza] = item.payload.split(',').map(Number);
            const timestamp = new Date(item.timestamp);

            newPhotodiodoPoints.push({ x: timestamp, y: photodiodo });
            newLatenzaPoints.push({ x: timestamp, y: latenza });
        });

        // Aggiungi i nuovi punti ai rispettivi grafici
        photodiodoChart.data.datasets[0].data.push(...newPhotodiodoPoints);
        latenzaChart.data.datasets[0].data.push(...newLatenzaPoints);

        // Mantieni solo gli ultimi MAX_POINTS punti
        [photodiodoChart, latenzaChart].forEach(chart => {
            chart.data.datasets.forEach(dataset => {
                if (dataset.data.length > MAX_POINTS) {
                    dataset.data = dataset.data.slice(-MAX_POINTS);
                }
            });
            chart.update();
        });

        updateView();
    }

    // Fetch dati
    function fetchData() {
        fetch("/realtime-data/")
            .then(response => {
                if (!response.ok) throw new Error('Network error');
                return response.json();
            })
            .then(data => processData(data))
            .catch(error => {
                console.error('Error:', error);
                statusPhotodiodo.innerHTML = statusLatenza.innerHTML = `
                    <i class="uil uil-exclamation-triangle mr-2"></i>
                    <span>Errore nel caricamento dati</span>
                `;
            });
    }

    // Polling ogni secondo
    const intervalId = setInterval(fetchData, 1000);
    fetchData(); // Chiamata iniziale

    window.addEventListener('beforeunload', () => {
        clearInterval(intervalId);
    });
});