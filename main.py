import pandas as pd
import numpy as np
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

df = pd.read_csv('end_data.csv')

# changing data types to make line 54 work properly
df['imdb_score'] = df['imdb_score'].astype(str)
df['year'] = df['year'].astype(str)


# define a function that creates similarity matrix
def create_sim():
    # loading count matrix
    count_matrix = pickle.load(open('cosine_similarity.pickle', 'rb'))

    # creating a similarity score matrix
    sim = cosine_similarity(count_matrix)
    return df, sim


# defining a function that recommends 10 most similar movies
def recommendation(m):
    m = m.lower()
    # check if data and sim are already assigned
    try:
        sim.shape
    except:
        df, sim = create_sim()
    # check if the movie is in our database or not
    if m not in df['movie'].unique():
        return('This movie is not in our database.\nPlease check if you spelled it correct.')
    else:
        # getting the index of the movie in the dataframe
        i = df.loc[df['movie'] == m].index[0]

        # fetching the row containing similarity scores of the movie from similarity matrix and enumerate it
        lst = list(enumerate(sim[i]))

        # sorting this list in decreasing order based on the similarity score
        lst = sorted(lst, key=lambda x: x[1], reverse=True)

        # not taking the first index since it is the same movie
        lst = lst[1:11]

        # making an empty list that will contain all 10 movie recommendations
        l = []
        b = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append('  -  '.join([df['movie'][a], df['year'][a], df['imdb_score'][a]]))

        return l

# using Flask web framework to put my app on web

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/recommend", methods=['POST', 'GET'])
def recommend():
    movie = request.args.get('movie')
    r = recommendation(movie)
    movie = movie.upper()
    if type(r)==type('string'):
        return render_template('recommend.html', movie=movie, r=r, t='s')
    else:
        return render_template('recommend.html', movie=movie, r=r, t='l')



if __name__ == '__main__':
    app.run()
