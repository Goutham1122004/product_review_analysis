from flask import Flask, render_template, request
from textblob import TextBlob
from pymongo import MongoClient
from urllib.parse import quote


def create_app():
    app = Flask(__name__)

    client = MongoClient('mongodb://localhost:27017/')
    db = client['product_reviews']
    collection = db['reviews']
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            data = request.form
            product_name = data['productName']
            rating = int(data['rating'])
            review_text = data['review']
            recommendation = data['recommendation']

            analysis = TextBlob(review_text)
            sentiment_score = analysis.sentiment.polarity

            if sentiment_score > 0:
                sentiment = 'positive'
            elif sentiment_score == 0:
                sentiment = 'neutral'
            else:
                sentiment = 'negative'
                
            review_data = {
                'product_name': product_name,
                'rating': rating,
                'review': review_text,
                'recommendation': recommendation,
                'sentiment': sentiment
            }
            collection.insert_one(review_data)

            previous_reviews = list(collection.find())  # Convert cursor to list

            return render_template('index.html', message='Review submitted successfully.', sentiment=sentiment, previous_reviews=previous_reviews)
        else:
            previous_reviews = list(collection.find())  # Convert cursor to list

            return render_template('index.html', previous_reviews=previous_reviews)
    
    @app.route('/close_connection')
    def close_connection():
        client.close()
        return 'Connection closed.'
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
