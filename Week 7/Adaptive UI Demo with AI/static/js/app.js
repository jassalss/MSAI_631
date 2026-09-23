const themeButton = document.getElementById("themeButton");
const adaptiveMessage = document.getElementById("adaptiveMessage");
const statusText = document.getElementById("statusText");

// --------------------------------------------------
// Send interaction to Flask
// --------------------------------------------------

function sendInteraction(action) {
  fetch("/api/interaction", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      action: action,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Interaction recorded:", data);

      // Ask ML model for a new prediction
      loadMLPreference();
    })
    .catch((error) => {
      console.error("Error sending interaction:", error);
    });
}

// --------------------------------------------------
// Dark Mode
// --------------------------------------------------

themeButton.addEventListener("click", function () {
  document.body.classList.toggle("dark");

  if (document.body.classList.contains("dark")) {
    themeButton.textContent = "Light Mode";

    sendInteraction("Dark Mode Enabled");
  } else {
    themeButton.textContent = " Dark Mode";

    sendInteraction("Dark Mode Disabled");
  }
});

// --------------------------------------------------
// Feature selection
// --------------------------------------------------

function selectFeature(featureName) {
  adaptiveMessage.textContent =
    "You selected " + featureName + ". The system is learning your preference.";

  statusText.textContent = "User interaction detected: " + featureName;

  console.log("User selected:", featureName);

  sendInteraction(featureName);
}

// --------------------------------------------------
// Highlight preferred feature
// --------------------------------------------------

function highlightPreferredFeature(featureName) {
  // Remove old highlight
  document.querySelectorAll(".feature-card").forEach((card) => {
    card.classList.remove("preferred");
  });

  // Highlight predicted feature
  if (featureName === "Dashboard") {
    document.getElementById("dashboardCard").classList.add("preferred");
  } else if (featureName === "Analytics") {
    document.getElementById("analyticsCard").classList.add("preferred");
  } else if (featureName === "Settings") {
    document.getElementById("settingsCard").classList.add("preferred");
  }
}

// --------------------------------------------------
// Get ML prediction from Flask
// --------------------------------------------------

function loadMLPreference() {
  fetch("/api/ml-preference")
    .then((response) => {
      if (!response.ok) {
        throw new Error("ML API returned status " + response.status);
      }

      return response.json();
    })

    .then((data) => {
      console.log("ML result:", data);

      const prediction = data.prediction;

      // Update adaptive message
      if (prediction === "None") {
        adaptiveMessage.textContent =
          "The system needs more interaction data before adapting the interface.";

        statusText.textContent =
          "Collecting user behavior: " +
          data.total_interactions +
          " / 5 interactions.";
      } else {
        adaptiveMessage.textContent =
          "The interface has adapted to your preference for " +
          prediction +
          ".";

        statusText.textContent =
          "AI prediction: " +
          prediction +
          " | Interface adapted automatically.";
      }

      // Highlight predicted feature
      highlightPreferredFeature(prediction);

      // Display behavior information
      console.log("Dashboard clicks:", data.dashboard);

      console.log("Analytics clicks:", data.analytics);

      console.log("Settings clicks:", data.settings);
    })

    .catch((error) => {
      console.error("Could not load ML preference:", error);
    });
}

// --------------------------------------------------
// Load ML prediction when page opens
// --------------------------------------------------

document.addEventListener("DOMContentLoaded", function () {
  loadMLPreference();
});
