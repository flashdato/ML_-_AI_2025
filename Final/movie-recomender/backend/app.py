from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # This will allow the frontend to make requests to our backend

# Load the data and similarity matrix
movies_dict = pickle.load(open('static/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('static/similarity.pkl', 'rb'))

@app.route('/movies', methods=['GET'])
def get_movie_titles():
    """
    Returns a JSON list of all movie titles.
    """
    movie_list = movies['title'].tolist()
    return jsonify({'movie_titles': movie_list})

def recommend(movie):
    """
    This function takes a movie title and returns 5 similar movies.
    """
    try:
        # Get the index of the movie that matches the title
        movie_index = movies[movies['title'] == movie].index[0]
        
        # Get the pairwise similarity scores of all movies with that movie
        distances = similarity[movie_index]
        
        # Sort the movies based on the similarity scores
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        for i in movies_list:
            recommended_movies.append(movies.iloc[i[0]].title)
            
        return recommended_movies
    except IndexError:
        # This happens if the movie is not in our dataset
        return []

@app.route('/')
def home():
    return "Movie Recommendation API is running!"

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    movie_title = data.get('movie_title')
    
    if not movie_title:
        return jsonify({'error': 'Movie title is required'}), 400
        
    recommendations = recommend(movie_title)
    
    if not recommendations:
        return jsonify({'message': 'Movie not found or no recommendations available.'}), 404
        
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    # Use port 5001 to avoid conflicts with frontend dev servers
    app.run(debug=True, port=5001)