(function($, window) {
  // Change the upload form's callback URL when "csv_type" changes.
  if ($('input[name="csv_type"]').length) {
    $('input[name="csv_type"]').on('change', function() {
      var csv_type = $(this).val();
      if (csv_type) {
        var old_action = $('#csv-upload-form').attr('action');
        var new_action = old_action.replace(/(\/)([^\/]+)$/, '$1' + csv_type);
        $('#csv-upload-form').attr('action', new_action);
      }
    });
  }
}).call(this, jQuery, window);
