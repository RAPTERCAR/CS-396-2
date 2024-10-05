import { loadQuiz } from './quizpage.js';
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
        body: JSON.stringify({ searchTerm: searchTerm })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          const quizId = data.quizzes[0].id;
          window.location.href = `quiz?quiz_id=${quizId}`;
        } else {
          console.log('No quizzes found');
        }
      });
    }
  });

  document.getElementById('dash-button').addEventListener('click', function() {
    // Toggle the pop-out menu
    document.getElementById('score-menu').style.display = 'block';

    // Make an AJAX request to retrieve the user's scores
    fetch('/get_scores')
      .then(response => response.json())
      .then(data => {
        console.log(data);
        const scoreList = document.getElementById('score-list');
        scoreList.innerHTML = '';

        data.scores.forEach(score => {
          const listItem = document.createElement('li');
          listItem.textContent = `${score['quiz_name']}: ${score['score']}%`;
          scoreList.appendChild(listItem);
        });
      })
  });
}
