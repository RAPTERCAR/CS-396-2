window.onload = function() {
  fetch('/data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({'request': 'getQuiz'})
  })
  .then(response => response.json())
  .then(data => {
    var html = '';
    for (var i = 0; i < data.length; i++) {
      html += '<li>' + data[i].name + ' (Time Limit: ' + data[i].time_limit + ')</li>';
    }
    document.getElementById('quizzes').innerHTML = html;
  })
  .catch(error => console.error('Error:', error));
  
  
  const searchInput = document.getElementById('search-input');
  const searchButton = document.getElementById('search-button');

  searchButton.addEventListener('click', () => {
    const searchTerm = searchInput.value.trim();
    if (searchTerm) {
      fetch('/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({searchTerm})
      })
      .then(response => response.json())
      .then(data => {
        if (data.length > 0) {
          // redirect to quiz page
          window.location.href = `/quiz/${data[0].id}`;
        } else {
          alert('No quiz found with that name');
        }
      })
    }
  });
}
