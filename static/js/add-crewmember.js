"use strict";

function addCrewMember() {
  $('#adding-crewmember').on('submit', (evt) => {
    evt.preventDefault();

    const formInputs = {
      'name': $('#user-name').val(),
      'role': $('#amount-field').val()
    };

    $.post('/add-crewmember/`{$project_id}', formInputs, (results) => {
      console.log(`Added: ${results}`);
    });
  });
}

addCrewMember();
