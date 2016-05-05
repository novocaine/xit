(function($, window) {
  var pollInterval = 500;

  /**
   * Shows a success or error message, and a "back home" link below it.
   */
  function showMessage(msg, status) {
    $('#csv-upload-container')
      .append(
        '<div class="alert alert-' + status + '">'
        + '<a class="close" title="Close" href="#" data-dismiss="alert">x</a>'
        + msg
        + '</div>');

    $('#csv-upload-container')
      .append(
        '<h2><a href="/">'
        + '<i class="fa fa-reply fa-fw" aria-hidden="true"></i>'
        + 'Back to upload form'
        + '</a></h2>');
  }

  function formatSuccess(body, code, action) {
    var xplan_url = $("#xplan_url").get(0).value;
    if (xplan_url[xplan_url.length-1] !== "/") {
        xplan_url += "/";
    }
    if (action === "/upload_csv/users") {
      if (code === 200) {
        label = "Updated user " + body.id;
      } else {
        label = "Created user " + body.id;
      }
      var user_url = xplan_url + "factfind/view/" + body.id + "?role=user";
      return "<a href='" + user_url + "'>" + label + "</a>";
    } else {
      if (code === 200) {
        verb = "Updated";
      } else {
        verb = "Created";
      }
      return verb + ": " + body.name + "(" + body.id + "): " + JSON.stringify(body.caps);
    }
  }

  function formatImportReportRow(response, action) {
    if (response.code === 200 || response.code === 201) {
        var body = $.parseJSON(response.body);
        return "<td class='success'>" + formatSuccess(body, response.code, action)
            + "</td>";
    } else {
        return "<td class='danger'>Failed: " + 
            response.msg +"</td>";
    }
  }

  /**
   * Shows a report of all response data from the resourceful API.
   */
  function showImportReport(data, action) {
    var reportHead = '<div class="table-responsive">'
      + '<table class="table table-hover table-striped">'
      + '<thead><tr>'
      + '<th>Response</th>'
      + '</tr></thead>'
      + '<tfoot><tr><th></th></tr></tfoot>'
      + '<tbody>';

    var reportFoot = '</tbody>'
      + '</table>'
      + '</div>';

    var reportBody = '';

    $.each(data, function(i, v) {
      reportBody += '<tr>'
        + formatImportReportRow(v, action)
        + '</tr>';
    });

    var report = reportHead + reportBody + reportFoot;

    $('#csv-upload-container').append(report);
  }

  /**
   * Polls the server at a regular interval to see if the task has finished.
   */
  function pollTaskStatus(task_uuid, action) {
    $.get('/task/' + task_uuid, function(data) {
      $('#loading-container').hide();

      if (data && data.length) {
        showMessage('Done!', 'success');
        showImportReport(data, action);
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
          $('#loading-container').hide();
          showMessage(jqXHR.responseText, 'danger');
        }

        // If we've made it down here, it means that the response was empty
        // (which is what triggers .fail(), there isn't any actual error
        // message / code). So, most likely it's a 102 "Processing" response
        // with empty body, so keep polling.
        else {
          setTimeout(function() {
            pollTaskStatus(task_uuid, action);
          }, pollInterval);
        }
      });
  }

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

  // Form submit handler stuff.
  if ($('#csv-upload-form').length) {
    $('#csv-upload-form').on('submit', function() {
      // Thanks to: http://stackoverflow.com/a/10899796
      var form_data = new FormData($(this)[0]);

      $('#front-page').hide();

      // Funky loader.
      $('#csv-upload-container')
        .append(
          '<div id="loading-container" class="text-center">'
          + '<i class="fa fa-cog fa-spin fa-3x fa-fw" aria-hidden="true"'
          + 'style="animation: fa-spin 4s infinite linear"></i>'
          + '<span class="sr-only">Importing. Hang tight!</span>'
          + '</div>');

      var action = $(this).attr('action');

      $.ajax({
        url: action,
        type: 'POST',
        data: form_data,
        async: false,
        success: function(data) {
          setTimeout(function() {
            pollTaskStatus(data, action);
          }, pollInterval);
        },
        cache: false,
        contentType: false,
        processData: false})
        .fail(function(jqXHR, textStatus, errorThrown) {
          $('#loading-container').hide();
          showMessage(errorThrown, 'danger');
        });

      return false;
    });
  }

  // Access level dump
  $("#download-access-levels").on('click', function() {
    var xplan_url = $("#xplan_url").get(0).value;
    if (xplan_url.length === 0) {
        $(this).parent().before("<div class='alert alert-warning'>Please enter your XPLAN URL above.</div>");
        return;
    }
    $(this).parent().parent().children(".alert").remove();
    window.location.href = "/access_levels?xplan_url=" + xplan_url + 
      "&xplan_username=" + $("#xplan_username").get(0).value + 
      "&xplan_password=" + $("#xplan_password").get(0).value;
  }); 
}).call(this, jQuery, window);
