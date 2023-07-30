from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
animes = pickle.load(open('animes.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           anime_name = list(popular_df['name'].values),
                           num_ratings = list(popular_df['num_ratings'].values),
                           rating = list(popular_df['avg_ratings'].values),
                           genre = list(popular_df['genre'].values),
                           type = list(popular_df['type'].values),
                           episodes = list(popular_df['episodes'].values),
                           image = list(popular_df['image_url'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_animes', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key = lambda x:x[1], reverse=True)[1:11]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = animes[animes['name'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('name')['name'].values))
        item.extend(list(temp_df.drop_duplicates('name')['genre'].values))
        item.extend(list(temp_df.drop_duplicates('name')['type'].values))
        item.extend(list(temp_df.drop_duplicates('name')['image_url'].values))
        
        data.append(item)
    
    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)