document.addEventListener('DOMContentLoaded', function () {
    const brandSelect = document.getElementById('id_brand');
    const modelSelect = document.getElementById('id_model');

    brandSelect.addEventListener('change', function () {
        const brand = this.value;

        fetch(`/experiments/get-models/?brand=${brand}`)
            .then(response => response.json())
            .then(data => {
                modelSelect.innerHTML = '<option value="">--- Seleziona ---</option>';
                data.models.forEach(model => {
                    const option = document.createElement('option');
                    option.value = model;
                    option.textContent = model;
                    modelSelect.appendChild(option);
                });
            });
    });
});