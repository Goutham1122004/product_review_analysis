

from flask import Flask, render_template, request
from textblob import TextBlob

app = Flask(__name__)

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
            
        # Mocking review submission
        message = 'Review submitted successfully.'
        previous_reviews = [
            {
                'product_name': product_name,
                'rating': rating,
                'review': review_text,
                'recommendation': recommendation,
                'sentiment': sentiment
            }
        ]

        return render_template('index.html', message=message, sentiment=sentiment, previous_reviews=previous_reviews)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
