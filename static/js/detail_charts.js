function renderDetailCharts(photodiodeData, latencyData) {
    const pdCtx = document.getElementById('photodiode-chart').getContext('2d');
    new Chart(pdCtx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Photodiode',
                data: photodiodeData,
                borderColor: 'rgb(54, 162, 235)',
                fill: false,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            parsing: { xAxisKey: 'x', yAxisKey: 'y' }
        }
    });

    const latCtx = document.getElementById('latency-chart').getContext('2d');
    new Chart(latCtx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Latency',
                data: latencyData,
                borderColor: 'rgb(255, 99, 132)',
                fill: false,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            parsing: { xAxisKey: 'x', yAxisKey: 'y' }
        }
    });
}
