document.addEventListener('DOMContentLoaded', function() {
    const brandSelect = document.getElementById('id_brand');
    const modelSelect = document.getElementById('id_model');
    const modeSelect = document.getElementById('id_mode');
    const experimentSelect = document.getElementById('id_experiment');

    function fetchModels(brand) {
        fetch(`/experiments/get-models/?brand=${encodeURIComponent(brand)}`)
            .then(resp => resp.json())
            .then(data => {
                modelSelect.innerHTML = '<option value="">---</option>';
                data.models.forEach(m => {
                    const option = document.createElement('option');
                    option.value = m;
                    option.textContent = m;
                    modelSelect.appendChild(option);
                });
            });
    }

    function fetchExperiments(brand, model, mode) {
        if (!brand || !model || !mode) {
            experimentSelect.innerHTML = '<option value="">---</option>';
            return;
        }
        fetch(`/experiments/get-experiments/?brand=${encodeURIComponent(brand)}&model=${encodeURIComponent(model)}&mode=${encodeURIComponent(mode)}`)
            .then(resp => resp.json())
            .then(data => {
                experimentSelect.innerHTML = '<option value="">---</option>';
                data.experiments.forEach(exp => {
                    const option = document.createElement('option');
                    option.value = exp.id;
                    option.textContent = exp.label;
                    experimentSelect.appendChild(option);
                });
            });
    }

    brandSelect.addEventListener('change', function() {
        const brand = this.value;
        if (brand) {
            fetchModels(brand);
        } else {
            modelSelect.innerHTML = '<option value="">---</option>';
            experimentSelect.innerHTML = '<option value="">---</option>';
        }
    });

    modelSelect.addEventListener('change', () => {
        fetchExperiments(brandSelect.value, modelSelect.value, modeSelect.value);
    });

    modeSelect.addEventListener('change', () => {
        fetchExperiments(brandSelect.value, modelSelect.value, modeSelect.value);
    });
});
