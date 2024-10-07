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
      
      //  Display the questions and answers

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
  //check all inputed answers
  questions.forEach((question, questionIndex) => {
    const selectedAnswer = question.querySelector('input[type="radio"]:checked');
    if (selectedAnswer) {
      answers[questionIds[questionIndex]] = selectedAnswer.value;
    } else {
      answers[questionIds[questionIndex]] = null;
    }
  });

  // Remove the quiz content and submit button
  const quizContainer = document.getElementById('quiz-container');
  quizContainer.style.display = 'none';

  fetch(`/submit_quiz/${quizId}`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ answers: answers })
  })
  .then(response => response.json())
  .then(data => {
      const score = data.score;
      const quizId = data.quiz_id;
      
      // Display the score to the user
      const resultElement = document.getElementById('result');
      resultElement.innerHTML = `You scored ${score}%!`;
      
      // Add a button to return to the home page
      const buttonElement = document.createElement('button');
      buttonElement.textContent = 'Return to Home Page';
      buttonElement.onclick = () => {
          window.location.href = 'home';
      };
      resultElement.appendChild(buttonElement);
      
      // Send the score and quiz ID to the /score endpoint
      fetch('/score', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ score: score, quiz_id: quizId })
      })
      .then(response => response.json())
      .then(data => {
          console.log('Score inserted successfully!');
      })
      .catch(error => {
          console.error('Error inserting score:', error);
      });
  })
  .catch(error => {
      console.error('Error submitting quiz:', error);
  });
}