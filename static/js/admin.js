window.onload=function(){    
    //creacte quiz
    document.getElementById('submitQ').addEventListener('click', function() {
        // Example AJAX call using fetch API
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
    //view all quizzes
    document.getElementById('viewAll').addEventListener('click', function() {
        // Example AJAX call using fetch API
        console.log('sending data');
        fetch('/data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'request': "viewAll",
        }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('test');
            document.getElementById('quizView').innerHTML = data.output;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
    //view spcific quiz
    document.getElementById('viewSpec').addEventListener('click', function() {
        // Example AJAX call using fetch API
        console.log('sending data');
        fetch('/data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'request': "viewSpec",
                'ID': document.getElementById('vSpec').value,
        }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('test');
            document.getElementById('quizView').innerHTML = data.output;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
    //add question
    document.getElementById('addQue').addEventListener('click', function() {
        // Example AJAX call using fetch API
        console.log('sending data');
        fetch('/data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'request': "addQue",
                'ID': document.getElementById('vSpec').value,
                'Det': document.getElementById('qdet').value
        }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('test');
            document.getElementById('quizView').innerHTML = data.display;
            document.getElementById('output').innerHTML = data.output;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
    //add answer
    document.getElementById('addAns').addEventListener('click', function() {
        // Example AJAX call using fetch API
        console.log('sending data');
        let x = 0;
        if(document.getElementById('isCor').checked == true){
            x = 1;
        }
        fetch('/data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'request': "addAns",
                'ID': document.getElementById('queid').value,
                'Det': document.getElementById('adet').value,
                'Cor': x
        }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('test');
            document.getElementById('quizView').innerHTML = data.display;
            document.getElementById('output').innerHTML = data.output;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}