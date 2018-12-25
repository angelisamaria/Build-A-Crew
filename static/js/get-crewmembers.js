function initUpdateStatusHandler() {
  $('#update-status').on('click', () => {

    // Our GET request URL will look like this:
    //       /status?order=123
    $.get('/status', {order: 123}, (results) => {
      console.log(`Result from server: ${results}`);

      const status = results;
      $('#order-status').html(status);

      console.log('Callback function finished');
    });

    console.log('GET request sent to server');
  });
}

initUpdateStatusHandler();