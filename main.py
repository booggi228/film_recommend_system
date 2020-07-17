import pandas as pd
import numpy as np
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv('cleaned_data.csv')

# remove symbols and adding a new column

df['movie'] = df['movie'].apply(lambda x: x.replace(':', '').replace('.', '').replace('-', '').replace('/', '').replace(',', '').lower().strip())

df['actors'] = df['actors'].astype(str)

df['description'] = df['description'].apply(lambda x: x.replace(',', '').replace('.', '').lower().strip())

df['actors'] = df['actors'].apply(lambda x: x.replace(',', '').replace('.', '').strip())
df['actors'] = df['actors'].astype(str)

df['imdb'] = df['imdb'].astype(str)

df['year'] = df['year'].astype(str)

df['score'] = 'imdb score'

df['imdb_score'] = df['score'].str.cat(df['imdb'], sep=" ")

df['genre'] = df['genre'].apply(lambda x: x.strip())

features = ['description', 'genre', 'actors']

# create new column with combined features
def combine_features(row):
    return row['description'] + ' ' + row['genre'] + ' ' + row['actors']

df['combined_features'] = df.apply(combine_features, axis=1)


# creating a similarity score matrix
def create_sim():
    # creating a count matrix
    cv = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
    count_matrix = cv.fit_transform(df['combined_features'])
    # creating a similarity score matrix
    sim = cosine_similarity(count_matrix)
    return sim


# defining a function that recommends 10 most similar movies
def recommendation(m):
    m = m.lower()
    # check if data and sim are already assigned
    try:
        sim.shape
    except:
        sim = create_sim()
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

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/recommend")
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

