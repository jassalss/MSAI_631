// This code is written by referencing AI tools
// like ChatGPT and google gemini
const myMovieInput = document.getElementById("movieInput");

const myRecommendButton = document.getElementById("recommendButton");

const myRecommendationsContainer = document.getElementById("recommendations");

const statusMessage = document.getElementById("statusMessage");

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
    const response = await fetch("/recommend", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        title: movieTitle,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Something went wrong.");
    }

    displayRecommendations(data.recommendations);

    statusMessage.textContent = `Recommendations for "${data.movie}"`;
  } catch (error) {
    myRecommendationsContainer.innerHTML = `
            <div class="error-message">
                ${error.message}
            </div>
        `;

    statusMessage.textContent = "Unable to get recommendations.";
  } finally {
    recommendButton.disabled = false;
  }
}

function displayRecommendations(recommendations) {
  myRecommendationsContainer.innerHTML = "";

  if (!recommendations || recommendations.length === 0) {
    myRecommendationsContainer.innerHTML = `
            <div class="error-message">
                No recommendations found.
            </div>
        `;

    return;
  }

  recommendations.forEach((movie, index) => {
    const card = document.createElement("div");

    card.className = "movie-card";

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

    myRecommendationsContainer.appendChild(card);
  });
}

myMovieInput.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    getRecommendations();
  }
});
