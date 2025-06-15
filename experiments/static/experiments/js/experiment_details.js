document.addEventListener('DOMContentLoaded', () => {
    const photodiodeLabels = JSON.parse(document.getElementById('photodiode-labels').textContent);
    const photodiodeValues = JSON.parse(document.getElementById('photodiode-values').textContent);
    const latencyLabels = JSON.parse(document.getElementById('latency-labels').textContent);
    const latencyValues = JSON.parse(document.getElementById('latency-values').textContent);

    const pdCtx = document.getElementById('photodiodeChart').getContext('2d');
    const latencyCtx = document.getElementById('latencyChart').getContext('2d');

    new Chart(pdCtx, {
        type: 'line',
        data: {
            labels: photodiodeLabels,
            datasets: [{
                label: 'Valori Photodiode',
                data: photodiodeValues,
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.3,
                fill: false,
                pointRadius: 2,
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Indice' } },
                y: { title: { display: true, text: 'Valore' } }
            }
        }
    });

    new Chart(latencyCtx, {
        type: 'line',
        data: {
            labels: latencyLabels,
            datasets: [{
                label: 'Latenza (μs)',
                data: latencyValues,
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                tension: 0.3,
                fill: false,
                pointRadius: 2,
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Indice' } },
                y: { title: { display: true, text: 'Valore (μs)' } }
            }
        }
    });
});
