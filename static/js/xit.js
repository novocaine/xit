(function($, window) {
  var pollInterval = 500;

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
  
  function showMessage(msg, status) {
    $('#csv-upload-form')
      .append(
        '<div class="alert alert-' + status + '">'
        + '<a class="close" title="Close" href="#" data-dismiss="alert">x</a>'
        + msg
        + '</div>');
  }
  
  function pollTaskStatus(task_uuid) {
    $.get('/task/' + task_uuid, function(data) {
      $('#csv-upload-submit').removeAttr('disabled');

      if (data && data.length && data[0].code &&
          data[0].code >= 200 && data[0].code <= 299) {
        showMessage('Done!', 'success');
        $('#csv-upload-form').trigger('reset');
      }
      else {
        // Unexpected if the server returns "success" but data has no
        // "OK" messages.
        var msg = (data && data.length && data[0].msg)
          ? data[0].msg
          : 'No data was imported';
        showMessage(msg, 'danger');
      }})
      .fail(function(jqXHR) {
        // Server has returned an actual error (e.g. could be a 500),
        // So handle it as such.
        if (jqXHR.responseText || jqXHR.status) {
          $('#csv-upload-submit').removeAttr('disabled');
          showMessage(jqXHR.responseText, 'danger');
        }

        // If we've made it down here, it means that the response was empty
        // (which is what triggers .fail(), there isn't any actual error
        // message / code). So, most likely it's a 102 "Processing" response
        // with empty body, so keep polling.
        else {
          setTimeout(function() {
            pollTaskStatus(task_uuid);
          }, pollInterval);
        }
      });
  }
  
  if ($('#csv-upload-form').length) {
    $('#csv-upload-form').on('submit', function() {
      // Thanks to: http://stackoverflow.com/a/10899796
      var form_data = new FormData($(this)[0]);
      
      $('#csv-upload-submit').attr('disabled', 'disabled');

      $.ajax({
        url: $(this).attr('action'),
        type: 'POST',
        data: form_data,
        async: false,
        success: function(data) {
          setTimeout(function() {
            pollTaskStatus(data);
          }, pollInterval);
        },
        cache: false,
        contentType: false,
        processData: false})
        .fail(function(jqXHR, textStatus, errorThrown) {
          $('#csv-upload-submit').removeAttr('disabled');
          showMessage(errorThrown, 'danger');
        });

      return false;
    });
  }
}).call(this, jQuery, window);
