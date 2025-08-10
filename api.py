from flask import Flask, request, jsonify
from genai_fetch import get_tournaments

app = Flask(__name__)

@app.route("/api/tournaments", methods=["GET"])
def tournaments_api():
    # Get 'sport' parameter from query string, default to "Cricket"
    sport = request.args.get("sport", "Cricket")

    # Call your existing GenAI fetch function
    data = get_tournaments(sport)

    # Return JSON response
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
