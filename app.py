import os
from flask import Flask
from database import db  # Import db from database.py
from flask_migrate import Migrate  # Import Flask-Migrate
from blueprints.main import main as main_blueprint





# Create Flask app
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, instance_path=os.path.join(basedir, 'instance'))

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'lms.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')

# Initialize Database
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
