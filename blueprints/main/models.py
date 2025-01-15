from database import db  # Import the SQLAlchemy instance
from datetime import datetime  # For timestamps

# ==========================
# Association Table for Many-to-Many Relationship
# ==========================
user_locations = db.Table(
    'user_locations',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('location_id', db.Integer, db.ForeignKey('location.id'), primary_key=True)
)

# ==========================
# User Model
# ==========================
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    job_title_id = db.Column(db.Integer, db.ForeignKey('job_title.id'))
    job_title = db.relationship('JobTitle', backref='users')  # Add this line
    role = db.Column(db.String(50))
    password = db.Column(db.String(255))
    code = db.Column(db.String(255))
    status = db.Column(db.String(50))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship('Company', backref='users')
 # Matches the 'company_id' field




    # Relationship to locations (Many-to-Many)
    locations = db.relationship(
        'Location',
        secondary=user_locations,
        backref=db.backref('users', lazy='dynamic'),
        lazy='dynamic'
    )

    def set_password(self, password):
        """Hash and set the user's password."""
        from werkzeug.security import generate_password_hash
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verify the user's password."""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.email}')"



# ==========================
# Qualification Model
# ==========================
class Qualification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    valid_days = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Qualification {self.name}>"


# ==========================
# Location Model
# ==========================
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"Location('{self.name}')"


# ==========================
# Company Model
# ==========================
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Company {self.name}>"


# ==========================
# Module Model
# ==========================
class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    file_name = db.Column(db.String(150), nullable=False)  # Extracted folder name
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ==========================
# Job Title Model
# ==========================
class JobTitle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<JobTitle {self.name}>"


# ==========================
# User Group Model
# ==========================
class UserGroup(db.Model):
    __tablename__ = 'user_group'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserGroup {self.name}>'

# Association table
user_group_association = db.Table('user_group_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('user_group.id'))
)
