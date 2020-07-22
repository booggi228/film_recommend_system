# Content-Based Film Recommend System: Project Overview
  * I've created a [film recommend system](https://film-recommend-system.ew.r.appspot.com/) for my own purposes as I'm a huge movie fan.  
  * Scraped over 25000 movies from 1990 to 2019 with IMDB rating above 5 from IMDB website using python and beautifullsoup.  
    Here is a [link](https://medium.com/better-programming/how-to-scrape-multiple-pages-of-a-website-using-a-python-web-scraper-4e2c641cff8) to scraper I used with some additional changes I made.  
  * After cleaning the data and removing duplicates there are a bit over 9000 films to work with.  
  * The details of the movies are: movie title, genre, runtime, IMDB rating, total votes, cast names, film overview.  
  * Built flask web application and deploy it on google cloud platform.    
  * **Packages I used:** pandas, numpy, sklearn, flask, pickle, beautifulsoup, gunicorn.  
  * Link to my application: https://film-recommend-system.ew.r.appspot.com/  
  
  
## About recommend system I used and how it works.  
   In this project I used content-based recommender system which suggest similar films based on particular keywords. In my case the system uses movie description, actor and director names, genres data to make these recommendations. To achieve this, I used [cosine similarity](https://www.machinelearningplus.com/nlp/cosine-similarity/) metric for all movies to to measure the distance between the embeddings which is needed for finding similarity between two movies. For that I created a new column named `combined_features` in the dataset which includes all the features I want to find the similarity score between items.  
  
  
## How to run the project?
  * Install all the libraries with command `pip install -r requirements.txt`.   
  * Clone this repository in your local system.  
  * Open the command prompt from your project directory and run the command `python main.py`.  
  * Go to your browser and type http://127.0.0.1:5000/ in the address bar.  
  * **That's all! Enjoy!**
  
