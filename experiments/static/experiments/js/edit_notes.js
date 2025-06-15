document.addEventListener("DOMContentLoaded", function () {
    const brandField = document.getElementById("id_brand");
    const modelField = document.getElementById("id_model");
    const experimentField = document.getElementById("id_experiment");

    brandField.addEventListener("change", function () {
        const brand = this.value;
        fetch(`/experiments/get-models/?brand=${brand}`)
            .then(res => res.json())
            .then(data => {
                modelField.innerHTML = `<option value="">--- Seleziona ---</option>`;
                data.models.forEach(model => {
                    modelField.innerHTML += `<option value="${model}">${model}</option>`;
                });
                experimentField.innerHTML = `<option value="">--- Seleziona ---</option>`;
            });
    });

    modelField.addEventListener("change", function () {
        const brand = brandField.value;
        const model = this.value;
        if (brand && model) {
            fetch(`/experiments/get-experiments/?brand=${brand}&model=${model}`)
                .then(res => res.json())
                .then(data => {
                    experimentField.innerHTML = `<option value="">--- Seleziona ---</option>`;
                    data.experiments.forEach(exp => {
                        experimentField.innerHTML += `<option value="${exp.id}">${exp.label}</option>`;
                    });
                });
        }
    });
});
