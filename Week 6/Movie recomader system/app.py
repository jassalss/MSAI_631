from flask import Flask, jsonify, request, render_template

from recommender import my_movie_recomnander, new_movies

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    data=request.get_json()
    my_title = data.get("title", "")
    if not my_title:
        return jsonify({
            "error: please provide the movie title"
        })
    movies_recommendations= my_movie_recomnander(my_title, 10)
    if not movies_recommendations:
        return jsonify({
            "error": f"Movie '{my_title}' was not found."
    }), 404
    return jsonify({
    "movie": my_title,
    "recommendations": movies_recommendations
})

@app.route("/api/test")
def api_test():
    return jsonify({
        "status": "success",
        "message": "Movie recommender API is working!"
    })
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )