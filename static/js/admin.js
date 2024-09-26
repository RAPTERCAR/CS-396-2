document.getElementById('submitQ').addEventListener('click', function() {
    // Example AJAX call using fetch API
    document.getElementById('msgs').innerHTML = '';
    console.log('sending data');
    fetch('/ajaxkeyvalue', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'qName': document.getElementById('qName').value,
                               "tLimit": document.getElementById('tLimit').value}),
    })
    .then(response => response.json())
    .then(data => {
      if (data.status == 'ok') {
          // Redirect to /library on success
          window.location.href = 'home';
      } else {
        // Update the 'msgs' div with the error message
         document.getElementById('msgs').innerHTML = '<p style= "color:red;">Error: ..........</p>';
      }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});