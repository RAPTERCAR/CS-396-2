window.onload=function(){   
    document.getElementById('login').addEventListener('click', function() {
        // Example AJAX call using fetch API
        document.getElementById('msgs').innerHTML = '';
        console.log('sending data');
        fetch('/ajaxkeyvalue', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'username': document.getElementById('username').value,
                                "password": document.getElementById('password').value}),
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
    document.getElementById('add').addEventListener('click', function() {
        // Example AJAX call using fetch API
        document.getElementById('msgs').innerHTML = '';
        console.log('sending data');
        let x = document.forms.cUsers.role.value;
        console.log(x);
        fetch('/data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'request': "addUser",
                                    'username': document.getElementById('addusername').value,
                                    "password": document.getElementById('addpassword').value,
                                    "fName": document.getElementById('addFName').value,
                                    "lName": document.getElementById('addLName').value,
                                    "role" : x
                                }),
        })
        .then(response => response.json())
        .then(data => {
        if (data.status == 'ok') {
            // Redirect to /library on success
            document.getElementById('msgs').innerHTML = '<p style= "color:green;">User Added</p>';
        } else {
            // Update the 'msgs' div with the error message
            document.getElementById('msgs').innerHTML = '<p style= "color:red;">Error: ..........</p>';
        }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}