let statsVisible = false;
    const statsButton = document.getElementById("stats-button");
    const statsContainer = document.getElementById("stats-container");

    statsButton.addEventListener("click", () => {
      if (!statsVisible) {
        statsContainer.innerHTML = "<h2>Statistics</h2>"; // placeholder for stats page
        statsVisible = true;
      } else {
        statsContainer.innerHTML = "";
        statsVisible = false;
      }
    });

const quizButton = document.getElementById("quiz-button");
quizButton.addEventListener("click", () => {
  window.location.href = 'quiz';

});