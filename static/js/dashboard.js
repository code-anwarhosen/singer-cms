// Product Distribution Chart
const productCtx = document.getElementById('productChart').getContext('2d');
const productChart = new Chart(productCtx, {
    type: 'doughnut',
    data: {
        labels: ['LG-OLED-55', 'SAMSUNG-380L', 'GREE-1.5TON', 'WALTON-8KG', 'SONY-43INCH'],
        datasets: [{
            data: [42, 35, 28, 22, 15],
            backgroundColor: ['#3B82F6', '#10B981', '#8B5CF6', '#F59E0B', '#EF4444'],
            borderColor: '#1F2937',
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        cutout: '70%',
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                backgroundColor: '#1F2937',
                titleColor: '#F3F4F6',
                bodyColor: '#D1D5DB',
                borderColor: '#374151',
                borderWidth: 1
            }
        }
    }
});
