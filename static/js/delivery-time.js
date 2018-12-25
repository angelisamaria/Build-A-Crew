"use strict";

// This function only exists to avoid creating global variables
function initDeliveryFormHandler() {
  $('#delivery-form').on('submit', evt => {
    evt.preventDefault();

    // Get user input from a form
    const formData = {
      city: $('#city-field').val(),
      address: $('#adr-field').val()
    };

    // Send formData to the server (becomes a query string)
    $.get('/delivery-info.json', formData, (results) => {

      // Remember, you can use console.dir to debug!
      // console.dir(results); 

      // Display results from the server
      alert(`This will cost $${results.cost}`);
      alert(`This will arrive in ${results.days} day(s)`);
    });
  });
}

initDeliveryFormHandler();
