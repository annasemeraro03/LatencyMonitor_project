document.addEventListener('DOMContentLoaded', function () {
    const brandField = document.querySelector('[name="brand"]');
    const modelField = document.querySelector('[name="model"]');

    brandField.addEventListener('change', function () {
        const selectedBrand = this.value;
        fetch(`/experiments/get-models/?brand=${encodeURIComponent(selectedBrand)}`)
            .then(response => response.json())
            .then(data => {
                modelField.innerHTML = '<option value="">--- Seleziona ---</option>';
                data.models.forEach(function (model) {
                    const option = document.createElement('option');
                    option.value = model;
                    option.textContent = model;
                    modelField.appendChild(option);
                });
            });
    });
});