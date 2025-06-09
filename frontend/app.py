from flask import Flask, render_template
from sqlalchemy.orm import sessionmaker, scoped_session
from models.models import Quote
import os


session_factory = Quote.build_engine()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    session = scoped_session(session_factory)
    quotes = session.query(Quote).all()
    return render_template('index.html', quotes=quotes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6300)
