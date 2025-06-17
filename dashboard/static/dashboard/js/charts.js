// static/js/charts.js

let comparisonChartPhotoInstance = null;
let comparisonChartVideoInstance = null;

function renderBrandPieChart(brandLabels, brandCounts) {
    const ctx = document.getElementById('brandPieChart')?.getContext('2d');
    if (!ctx) {
        console.warn('Elemento brandPieChart non trovato');
        return;
    }

    if (!Array.isArray(brandLabels) || brandLabels.length === 0) {
        brandLabels = ['Nessun dato'];
        brandCounts = [1];
    }
    if (!Array.isArray(brandCounts) || brandCounts.length === 0) {
        brandLabels = ['Nessun dato'];
        brandCounts = [1];
    }

    const backgroundColors = [
        'rgba(255, 99, 132, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)',
        'rgba(255, 159, 64, 0.7)',
        'rgba(199, 199, 199, 0.7)',
        'rgba(83, 102, 255, 0.7)',
        'rgba(40, 167, 69, 0.7)',
        'rgba(253, 126, 20, 0.7)'
    ];

    const borderColors = backgroundColors.map(color => color.replace('0.7', '1'));

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: brandLabels,
            datasets: [{
                data: brandCounts,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });
}

function renderComparisonChartPhoto(datasets) {
    const ctx = document.getElementById('comparisonChartPhoto').getContext('2d');

    if (!ctx) {
        console.warn('Elemento comparisonChart non trovato');
        return;
    }

    if (!Array.isArray(datasets) || datasets.length === 0) {
        datasets = [{
            label: 'Nessun dato',
            data: [],
            borderColor: 'rgba(200, 200, 200, 0.5)',
            tension: 0.3,
        }];
    }

    const maxLength = datasets.reduce((max, d) => Math.max(max, d.data.length), 0);
    const labels = Array.from({length: maxLength}, (_, i) => i + 1); 

    if (comparisonChartPhotoInstance) {
        comparisonChartPhotoInstance.data.labels = labels;
        comparisonChartPhotoInstance.data.datasets = datasets;
        comparisonChartPhotoInstance.update();
        return;
    }

    comparisonChartPhotoInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            },
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'Latency (µs)',
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Indice',
                    }
                }
            }
        }
    });
}

function renderComparisonChartVideo(datasets) {
    const ctx = document.getElementById('comparisonChartVideo').getContext('2d');

    if (!ctx) {
        console.warn('Elemento comparisonChart non trovato');
        return;
    }

    if (!Array.isArray(datasets) || datasets.length === 0) {
        datasets = [{
            label: 'Nessun dato',
            data: [],
            borderColor: 'rgba(200, 200, 200, 0.5)',
            tension: 0.3,
        }];
    }

    const maxLength = datasets.reduce((max, d) => Math.max(max, d.data.length), 0);
    const labels = Array.from({length: maxLength}, (_, i) => i + 1); 

    if (comparisonChartVideoInstance) {
        comparisonChartVideoInstance.data.labels = labels;
        comparisonChartVideoInstance.data.datasets = datasets;
        comparisonChartVideoInstance.update();
        return;
    }

    comparisonChartVideoInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            },
            scales: {
                y: {
                    // beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Latency (µs)',
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Indice',
                    }
                }
            }
        }
    });
}

function renderDetailCharts(photodiodeData, latencyData) {
    const pdCtx = document.getElementById('photodiode-chart')?.getContext('2d');
    if (pdCtx) {
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
                maintainAspectRatio: false,
                parsing: { xAxisKey: 'x', yAxisKey: 'y' },
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    x: {
                        type: 'linear',
                        title: { display: true, text: 'Indice' }
                    },
                    y: {
                        title: { display: true, text: 'Valore fotodiodo' }
                    }
                }
            }
        });
    }

    const latCtx = document.getElementById('latency-chart')?.getContext('2d');
    if (latCtx) {
        new Chart(latCtx, {
            type: 'line',
            data: {
                datasets: [{
                    label: 'Latency',
                    data: latencyData,
                    borderColor: 'rgb(54, 162, 235)',
                    fill: false,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                parsing: { xAxisKey: 'x', yAxisKey: 'y' },
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    x: {
                        type: 'linear',
                        title: { display: true, text: 'Indice' }
                    },
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Latenza' }
                    }
                }
            }
        });
    }
}

function renderExperimentCharts(data) {
    Object.keys(data).forEach(expId => {
        const ctx = document.getElementById(`chart-${expId}`)?.getContext('2d');
        if (!ctx) return;

        const chartInfo = data[expId];

        const formattedData = chartInfo.labels.map((label, index) => ({
            x: parseFloat(label),
            y: parseFloat(chartInfo.latency[index])
        }));

        new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: 'Latenza',
                    data: formattedData,
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    fill: false,
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                parsing: { xAxisKey: 'x', yAxisKey: 'y' },
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    x: {
                        type: 'linear',
                        title: { display: true, text: 'Indice' }
                    },
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Latenza (µs)' }
                    }
                }
            }
        });
    });
}

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i=0; i<6; i++) {
        color += letters[Math.floor(Math.random()*16)];
    }
    return color;
}
