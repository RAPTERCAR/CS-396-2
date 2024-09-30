const urlParams = new URLSearchParams(window.location.search);
const quizId = urlParams.get('quiz_id');

if (quizId) {
  loadQuiz(quizId);
}

export function loadQuiz(quizId) {
    fetch(`/quest/${quizId}`)
      .then(response => response.json())
      .then(data => {
        const quizContainer = document.getElementById('quiz-container');
        quizContainer.innerHTML = ''; // Clear the container before loading new quiz
        data.forEach(question => {
          const questionHTML = `
            <h2>${question.question[2]}</h2>
            <div class="answers">
            ${question.answers.map(answer => `
              <button class="answer-button">${answer[2]}</button>
            `).join('')}
            </div>
          `;
          quizContainer.innerHTML += questionHTML;
        });
      })
      .catch(error => console.error('Error:', error));
  }