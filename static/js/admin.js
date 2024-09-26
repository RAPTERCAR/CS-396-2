document.getElementById('submitQ').addEventListener('click', function() {
    // Example AJAX call using fetch API
    document.getElementById('msgs').innerHTML = '';
    console.log('sending data');
    fetch('/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'request': "createQuiz",
                               'qName': document.getElementById('qName').value,
                               "tLimit": document.getElementById('tLimit').value}),
    })
    .then(response => response.json())
    .then(data => {
        console.log('test');
        document.getElementById('output').innerHTML = data.output;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});