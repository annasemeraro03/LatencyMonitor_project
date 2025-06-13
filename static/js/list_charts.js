function renderExperimentCharts(data) {
    Object.keys(data).forEach(expId => {
        const ctx = document.getElementById(`chart-${expId}`).getContext('2d');
        const chartInfo = data[expId];

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartInfo.labels,
                datasets: [{
                    label: 'Latenza',
                    data: chartInfo.latency,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    fill: false,
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });
}
