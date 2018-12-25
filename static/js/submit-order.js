"use strict";

function addCrewMember() {
  $('#order-form').on('submit', (evt) => {
    evt.preventDefault();

    const formInputs = {
      'type': $('#type-field').val(),
      'amount': $('#amount-field').val()
    };

    $.post('/new-order', formInputs, (results) => {
      console.log(`Added: ${results}`);
    });
  });
}

addCrewMember();
