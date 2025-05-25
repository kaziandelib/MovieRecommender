from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# Load the serialized data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie_title):
    index = movies[movies['title'] == movie_title].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_titles = [movies.iloc[i[0]].title for i in distances[1:6]]
    return recommended_titles

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_movie = request.form['movie']
        recommendations = recommend(selected_movie)
        return render_template('index.html', movies=movies['title'].values, selected_movie=selected_movie, recommendations=recommendations)
    return render_template('index.html', movies=movies['title'].values, recommendations=[])

if __name__ == '__main__':
    app.run(debug=True)
