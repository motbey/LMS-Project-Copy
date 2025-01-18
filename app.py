import os
from datetime import datetime
from flask import Flask, g, session
from flask_migrate import Migrate
from database import db
from blueprints.main import main as main_blueprint
from blueprints.main.auth import auth as auth_blueprint
from blueprints.main.models import User

# Create Flask app
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, 
    static_url_path='/static',
    static_folder='static',
    instance_path=os.path.join(basedir, 'instance'))

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'lms.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Initialize Database
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)

@app.before_request
def before_request():
    if 'user_id' in session:
        try:
            user = User.query.get(session['user_id'])
            if user:
                user.last_seen = datetime.utcnow()
                try:
                    db.session.commit()
                except Exception:
                    db.session.rollback()
        except Exception:
            db.session.rollback()

if __name__ == '__main__':
    app.run(debug=True)
