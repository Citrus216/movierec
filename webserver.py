from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp import get_recommendations

app = Flask(__name__)
CORS(app)

# Endpoint to get all movies
@app.route('/api/v1/movies', methods=['GET'])
def get_movies():
    query = request.args.get('query', default='', type=str)
    return jsonify({'movies': get_recommendations(query, recalc=False)})


if __name__ == '__main__':
    app.run(debug=True)
