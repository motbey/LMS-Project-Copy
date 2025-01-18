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
    last_seen = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
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

# ==========================
# Group Rule Model
# ==========================
class GroupRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'role', 'company', 'job_title', 'location'
    value = db.Column(db.String(50), nullable=False)  # ID or value of the selected item
    
    group = db.relationship('UserGroup', backref=db.backref('rules', lazy=True))

# ==========================
# User Group Criteria Model
# ==========================
class UserGroupCriteria(db.Model):
    __tablename__ = 'user_group_criteria'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('user_group.id', ondelete='CASCADE'), nullable=False)
    criteria_type = db.Column(db.String(50), nullable=False)  # 'role', 'company', 'location', 'job_title', 'code'
    criteria_value = db.Column(db.String(50), nullable=False)
    
    group = db.relationship('UserGroup', backref=db.backref('criteria', lazy=True))

# ==========================
# User Group Member Model
# ==========================
class UserGroupMember(db.Model):
    __tablename__ = 'user_group_member'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    group = db.relationship('UserGroup', backref=db.backref('members', lazy=True))
    user = db.relationship('User', backref=db.backref('group_memberships', lazy=True))

    def __repr__(self):
        return f'<UserGroupMember {self.group_id}:{self.user_id}>'

# ==========================
# Group Qualification Model
# ==========================
class GroupQualification(db.Model):
    __tablename__ = 'group_qualification'
    
    group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'), primary_key=True)
    qualification_id = db.Column(db.Integer, db.ForeignKey('qualification.id'), primary_key=True)
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='Active')
    
    # Relationships
    group = db.relationship('UserGroup', backref=db.backref('group_qualifications', lazy=True))
    qualification = db.relationship('Qualification', backref=db.backref('group_qualifications', lazy=True))

# ==========================
# Group Module Model
# ==========================
class GroupModule(db.Model):
    __tablename__ = 'group_module'
    
    group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'), primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), primary_key=True)
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    required_completion_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='Active')

    # Relationships
    group = db.relationship('UserGroup', backref=db.backref('group_modules', lazy=True))
    Module = db.relationship('Module', backref=db.backref('group_modules', lazy=True))

# Add these model classes to your existing models.py file
from datetime import datetime

class UserModule(db.Model):
    __tablename__ = 'user_modules'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='Assigned')

    # Add these relationships
    user = db.relationship('User', backref=db.backref('user_modules', lazy=True))
    module = db.relationship('Module', backref=db.backref('user_modules', lazy=True))

class UserQualification(db.Model):
    __tablename__ = 'user_qualifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    qualification_id = db.Column(db.Integer, db.ForeignKey('qualification.id'), nullable=False)
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='Assigned')

    # Add these relationships
    user = db.relationship('User', backref=db.backref('user_qualifications', lazy=True))
    qualification = db.relationship('Qualification', backref=db.backref('user_qualifications', lazy=True))
