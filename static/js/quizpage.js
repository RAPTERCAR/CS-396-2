const urlParams = new URLSearchParams(window.location.search);
const quizId = urlParams.get('quiz_id');
let questionIds = [];

if (quizId) {
  loadQuiz(quizId);
}

export function loadQuiz(quizId) {
  fetch(`/quest/${quizId}`)
    .then(response => response.json())
    .then(data => {
      const quizContainer = document.getElementById('quiz-container');
      quizContainer.innerHTML = ''; // Clear the container before loading new quiz
      questionIds = data.questions.map(question => question.question[0]);

      // Display the time limit
      let timeLimit = data.time_limit * 60; // Convert minutes to seconds
      let timerHTML = `
        <h3 id="timer">Time Limit: ${formatTime(timeLimit)}</h3>
      `;
      quizContainer.innerHTML += timerHTML;
      
      // Start the countdown timer
      let timerInterval = setInterval(() => {
        timeLimit--;
        document.getElementById('timer').innerHTML = `Time Limit: ${formatTime(timeLimit)}`;
        if (timeLimit <= 0) {
          clearInterval(timerInterval);
          window.location.href = 'home';
        }
      }, 1000);
      
      data.questions.forEach((question, questionIndex) => {
        const questionHTML = `
          <h2>${question.question[2]}</h2>
          <div class="answers">
          ${question.answers.map((answer, answerIndex) => `
            <input type="radio" id="answer-${questionIndex}-${answerIndex}" name="answer-${questionIndex}" value="${answer[2]}">
            <label for="answer-${questionIndex}-${answerIndex}">${answer[2]}</label>
          `).join('')}
          </div>
        `;
        quizContainer.innerHTML += questionHTML;
      });

      // Add a submit button
      const submitButtonHTML = `
      <button id="submit-button">Submit Quiz</button>
    `;
    quizContainer.innerHTML += submitButtonHTML;
    
    // Add an event listener to the submit button
    document.getElementById('submit-button').addEventListener('click', submitQuiz);
  })
}

// Helper function to format the time
function formatTime(seconds) {
  let minutes = Math.floor(seconds / 60);
  let remainingSeconds = seconds % 60;
  return `${minutes} : ${remainingSeconds}`;
}

// Function to submit the quiz
function submitQuiz() {
  const answers = {};
  const questions = document.querySelectorAll('.answers');
  questions.forEach((question, questionIndex) => {
    const selectedAnswer = question.querySelector('input[type="radio"]:checked');
    if (selectedAnswer) {
      answers[questionIds[questionIndex]] = selectedAnswer.value;
    } else {
      answers[questionIds[questionIndex]] = null;
    }
  });
  
  // Send the answers to the server
  fetch(`/submit_quiz/${quizId}`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ answers: answers })
  })
  .then(response => response.json())
  .then(data => {
      // Display the score
      const scoreHTML = `
        <h2>Your score is ${data.score} out of ${Object.keys(answers).length}.</h2>
        <button onclick="window.location.href = '/home';">Back to Home</button>
      `;
      document.getElementById('quiz-container').innerHTML = scoreHTML;
  })
}