from flask import Flask, render_template
from models.models import Session, Quote

app = Flask(__name__)

@app.route('/')
def index():
    session = Session()
    quotes = session.query(Quote).all()
    return render_template('index.html', quotes=quotes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
