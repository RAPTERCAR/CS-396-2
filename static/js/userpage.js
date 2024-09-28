const quizButtonsContainer = document.getElementById('quiz-buttons-container');
const quizButtonTemplate = document.getElementById('quiz-button-template');

fetch('/data', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ 'request': "getQuiz" }),
})
  .then(response => {
    if (!response.ok) {
      throw new Error(response.statusText);
    }
    return response.json();
  })
  .then(quizzes => {
    quizzes.forEach(quiz => {
      const quizButton = quizButtonTemplate.content.cloneNode(true);
      quizButton.querySelector('button').textContent = quiz.name;
      quizButton.querySelector('button').onclick = () => {
        window.location.href = `quiz.html`;
      };
      quizButtonsContainer.appendChild(quizButton);
    });
  })
  .catch(error => {
    console.error('Error:', error);
  });
