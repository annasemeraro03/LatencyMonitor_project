$(document).ready(function () {
  $('#id_brand').on('change', function () {
    const brand = $(this).val();
    $.ajax({
      url: urls.getModels,
      data: { brand: brand },
      success: function (data) {
        const modelSelect = $('#id_model');
        modelSelect.empty().append($('<option>').text('---------').attr('value', ''));
        data.models.forEach(function (model) {
          modelSelect.append($('<option>').text(model).attr('value', model));
        });
        $('#id_experiment').empty().append($('<option>').text('---------').attr('value', ''));
      }
    });
  });

  $('#id_model').on('change', function () {
    const brand = $('#id_brand').val();
    const model = $(this).val();
    $.ajax({
      url: urls.getExperiments,
      data: { brand: brand, model: model },
      success: function (data) {
        const expSelect = $('#id_experiment');
        expSelect.empty().append($('<option>').text('---------').attr('value', ''));
        data.experiments.forEach(function (exp) {
          expSelect.append($('<option>').text(exp.text).attr('value', exp.id));
        });
      }
    });
  });
});
