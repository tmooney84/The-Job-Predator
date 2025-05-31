from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration
user = 'root'
password = 'Safe+!st'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://{user}:{password}@127.0.0.1:3306/job_hunter'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.LargeBinary(16), primary_key=True)
    title = db.Column(db.String(255))
    company_id = db.Column(db.Integer)
    location = db.Column(db.String(45))
    description = db.Column(db.Text)
    salary = db.Column(db.String(45))
    source = db.Column(db.String(45))
    url = db.Column(db.String(255))
    status = db.Column(db.Enum('open', 'closed', 'unknown'))
    job_category_id = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company_id': self.company_id,
            'location': self.location,
            'description': self.description,
            'salary': self.salary,
            'source': self.source,
            'url': self.url,
            'status': self.status,
            'job_category_id': self.job_category_id
        }

@app.route('/api/all_jobs', methods=['GET'])
def get_jobs():
    try:
        jobs = Job.query.all()
        job_list = [job.to_dict() for job in jobs]
        return jsonify(job_list)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6300)
