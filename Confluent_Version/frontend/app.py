from flask import Flask, render_template
from models.models import Quote, Session, Engine
import os

DATABASE_URL = os.environ["DATABASE_URL"]
engine = Engine
session = Session

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    model = Quote()
    quotes = session.query(Quote).all()
    return render_template('index.html', quotes=quotes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6300)
