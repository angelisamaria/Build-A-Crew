"use strict";



document.addEventListener('keydown', function (event) {
  var esc = event.which == 27, // esc
      rtn = event.which == 13, // return
      el = event.target,
      input = el.nodeName != 'INPUT' && el.nodeName != 'TEXTAREA',
      data = {}; // empty json object

  if (input) {
    if (esc) {
      // restore to previous state
      document.execCommand('undo');
    el.blur();
    } else if (rtn) {
      // save changes
      data[el.getAttribute('data-name')] = el.innerHTML;

      // we could send an ajax request to update the field
      
    //   $.ajax({
    //     type: "POST",
    //     url: 'projects/newproject.html',
    //     data: ({ proj_desc: input }),
    //     dataType: "html",
    //     success: function(data) {
    //         // Run the code here that needs
    //         //    to access the data returned
    //         return data;
    //     },
    //     error: function() {
    //         alert('Error occured');
    //     }
    // });
      
      log(JSON.stringify(data));

      el.blur();
      event.preventDefault();
    }
  }
}, true);

function log(s) {
  document.getElementById('proj_logline').innerHTML = 'value changed to: ' + s;
}



