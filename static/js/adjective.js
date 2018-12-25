"use strict";

function getAdjective() {
  $.get('/adjective', (results) => {
    const adj = results;

    $('#adjective').html(adj);
  });
}

getAdjective();

