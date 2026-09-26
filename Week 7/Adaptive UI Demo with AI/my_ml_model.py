import sqlite3

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


DATABASE = "adaptive_ui.db"


def get_user_counts():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT action, COUNT(*)
        FROM interactions
        WHERE action IN (
            'Dashboard',
            'Analytics',
            'Settings'
        )
        GROUP BY action
    """)

    rows = cursor.fetchall()
    connection.close()

    dashboard = 0
    analytics = 0
    settings = 0

    for action, count in rows:

        if action == "Dashboard":
            dashboard = count

        elif action == "Analytics":
            analytics = count

        elif action == "Settings":
            settings = count

    return dashboard, analytics, settings


def create_training_data():

    X = []
    y = []

    # Create simulated examples.
    # The largest interaction count determines
    # the user's preferred feature.

    for dashboard in range(1, 21):
        for analytics in range(1, 11):
            for settings in range(1, 11):

                X.append([
                    dashboard,
                    analytics,
                    settings
                ])

                if dashboard > analytics and dashboard > settings:
                    y.append("Dashboard")

                elif analytics > dashboard and analytics > settings:
                    y.append("Analytics")

                elif settings > dashboard and settings > analytics:
                    y.append("Settings")

                else:
                    # Ignore ties
                    X.pop()
                    continue

    return X, y


def train_model():

    X, y = create_training_data()

    model = DecisionTreeClassifier(
        random_state=42,
        max_depth=5
    )

    model.fit(X, y)

    predictions = model.predict(X)

    accuracy = accuracy_score(
        y,
        predictions
    )

    print("Training samples:", len(X))
    print("Model accuracy:", accuracy)

    return model, accuracy


def predict_preference():

    dashboard, analytics, settings = get_user_counts()

    total_interactions = (
        dashboard +
        analytics +
        settings
    )

    print("\nUser behavior:")
    print("Dashboard:", dashboard)
    print("Analytics:", analytics)
    print("Settings:", settings)
    print("Total:", total_interactions)

    # Wait until enough behavior has been collected
    if total_interactions < 5:

        return {
            "dashboard": dashboard,
            "analytics": analytics,
            "settings": settings,
            "total_interactions": total_interactions,
            "prediction": "None",
            "accuracy": 0
        }

  
    model, accuracy = train_model()

    # Current user's behavior
    user_data = [[
        dashboard,
        analytics,
        settings
    ]]

    prediction = model.predict(user_data)[0]

    print("ML prediction:", prediction)

    return {
        "dashboard": dashboard,
        "analytics": analytics,
        "settings": settings,
        "total_interactions": total_interactions,
        "prediction": prediction,
        "accuracy": accuracy
    }