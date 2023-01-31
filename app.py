from flask import Flask, render_template,request
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

popular_df = pickle.load(open('popular_df.pkl','rb'))
popular_df = pd.DataFrame(popular_df)

similarity = pickle.load(open('similarity.pkl','rb'))
# print(similarity)

pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('book.pkl','rb'))
# print(pt)

def recommend(book):
    book_index = np.where(pt.index == book)
    
    data = []
    if len(book_index[0]) > 0 :
        book_index = book_index[0][0]
    else :
        return data


    top_book_suggestions = sorted(list(enumerate(similarity[book_index])),key=lambda x: x[1],reverse=True)[1:5]
    
    for i in top_book_suggestions:
        items = []
        
        temp_df = books[books['Book-Title']== pt.index[i[0]]]
        title = temp_df.drop_duplicates('Book-Title')['Book-Title'].values
        author = temp_df.drop_duplicates('Book-Title')['Book-Author'].values
        image_url = temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values
        items.extend(list(title))
        items.extend(list(author))
        items.extend(list(image_url))
        data.append(items)
    
    return data
print(recommend('dfkjask'))
@app.route('/')
def home():
    return render_template('home.html',df = (popular_df))

@app.route('/book_recommendation',methods=['GET','POST'])
def book_recommendation():
    book = request.form.get('book')
    data = recommend(book)
    return render_template('recommend.html',data=data)

if __name__ == "__main__" :
    app.run(debug=True)
