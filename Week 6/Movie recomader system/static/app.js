const myMovieInput = document.getElementById("movieInput");

const myRecommendButton = document.getElementById("recommendButton");

const myRecommendationsContainer = document.getElementById("recommendations");

const statusMessage = document.getElementById("statusMessage");

// ==========================================
// Get Movie Recommendations
// ==========================================

async function getRecommendations() {
  const movieTitle = movieInput.value.trim();

  if (!movieTitle) {
    statusMessage.textContent = "Please enter a movie title.";

    return;
  }

  statusMessage.textContent = "Finding similar movies...";

  myRecommendButton.disabled = true;
  myRecommendationsContainer.innerHTML = "";

  try {
    // Send request to Flask backend
    const response = await fetch("/recommend", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        title: movieTitle,
      }),
    });

    // Convert response to JSON
    const data = await response.json();

    // Check if Flask returned an error
    if (!response.ok) {
      throw new Error(data.error || "Something went wrong.");
    }

    // Display recommendations
    displayRecommendations(data.recommendations);

    // Update status
    statusMessage.textContent = `Recommendations for "${data.movie}"`;
  } catch (error) {
    // Show error message
    myRecommendationsContainer.innerHTML = `
            <div class="error-message">
                ${error.message}
            </div>
        `;

    statusMessage.textContent = "Unable to get recommendations.";
  } finally {
    // Enable button again
    recommendButton.disabled = false;
  }
}

// ==========================================
// Display Movie Recommendations
// ==========================================

function displayRecommendations(recommendations) {
  // Clear existing cards
  myRecommendationsContainer.innerHTML = "";

  // Check if there are no recommendations
  if (!recommendations || recommendations.length === 0) {
    myRecommendationsContainer.innerHTML = `
            <div class="error-message">
                No recommendations found.
            </div>
        `;

    return;
  }

  // Create a card for every movie
  recommendations.forEach((movie, index) => {
    const card = document.createElement("div");

    card.className = "movie-card";

    // Create movie card HTML
    card.innerHTML = `

                <h3>
                    ${index + 1}. ${movie.title}
                </h3>


                <div class="movie-info">

                    <span>
                        ${movie.release_year}
                    </span>

                    <span>
                        ${movie.rating}
                    </span>

                    <span>
                        ${movie.duration}
                    </span>

                </div>


                <div class="movie-info">

                    <span>
                        ${movie.genre}
                    </span>

                </div>


                <div class="similarity">

                    Similarity:
                    ${(movie.similarity * 100).toFixed(1)}%

                </div>


                <p class="movie-description">

                    ${movie.description}

                </p>
            `;

    // Add card to page
    myRecommendationsContainer.appendChild(card);
  });
}

myMovieInput.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    getRecommendations();
  }
});
