from flask import render_template, request, redirect, url_for, flash, session
from . import main  # Import the blueprint
from werkzeug.security import generate_password_hash
from database import db  # Import db from database.py
from blueprints.main.models import User  # Import User model
from flask import session
from werkzeug.security import check_password_hash
from .models import Qualification
from .models import Location # Import Location and User models
from flask import jsonify  # Import jsonify for JSON responses
from math import ceil
import pandas as pd  # Add this at the top if not already imported
from flask import request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from blueprints.main.models import Company  # Import the correct model
import logging
logging.basicConfig(level=logging.DEBUG)
from flask import send_from_directory
from flask import current_app
import zipfile
from lxml import etree
from .models import Module
from blueprints.main.models import JobTitle  # Adjust the path if needed


# Home route
@main.route('/')
def home():
    return render_template('home.html')

# Registration route
@main.route('/register', methods=['GET', 'POST'])
def register():
    # Fetch all available locations from the database
    locations = Location.query.all()

    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        company = request.form.get('company')
        code = request.form.get('code')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        location_id = request.form.get('location_id')  # Updated to get location ID

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('main.register'))

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered!', 'danger')
            return redirect(url_for('main.register'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user (Role is default 'User')
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            company=company,
            code=code,
            password=hashed_password,
            role="User",  # Default role
            status="Active"  # Default status
        )

        # Assign selected location to the user
        selected_location = Location.query.get(location_id)
        if selected_location:
            new_user.locations.append(selected_location)  # Use many-to-many relationship

        # Add user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('main.home'))

    # Render registration form with available locations
    return render_template('register.html', locations=locations)


from flask import session

# Dashboard Route
@main.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('main.home'))
    
    # Retrieve user details from session
    user = {
        'id': session.get('user_id'),  # <-- Added 'id' here
        'first_name': session.get('first_name'),
        'last_name': session.get('last_name'),
        'email': session.get('email'),
        'role': session.get('role')
    }

    # Debugging the user object
    print(user)  # Debug statement to verify the user object.

    return render_template('dashboard.html', user=user)



# Logout Route
@main.route('/logout')
def logout():
    session.clear()  # Clear all session data
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))


@main.route('/login', methods=['POST'])
def login():
    # Get form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Query database for the user
    user = User.query.filter_by(email=email).first()

    # Check if user exists
    if user:
        # Check if the user is active
        if user.status != 'Active':
            flash('Your account has been locked. Please contact the Administrator.', 'danger')
            return redirect(url_for('main.home'))

        # Check if the password matches
        if check_password_hash(user.password, password):
            # Store user details in session
            session['user_id'] = user.id
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            session['email'] = user.email
            session['role'] = user.role  # Assign role from DB

            flash('Login successful!', 'success')

            # Redirect based on role
            if user.role == 'Admin':
                return redirect(url_for('main.admin_dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            # Invalid password
            flash('Invalid email or password. Please try again.', 'danger')
    else:
        # User not found
        flash('Invalid email or password. Please try again.', 'danger')

    return redirect(url_for('main.home'))



# Admin Dashboard Route
@main.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    try:
        # Retrieve filter values from form inputs
        filters = {
            'id': request.args.get('id', '').strip(),
            'first_name': request.args.get('first_name', '').strip(),
            'last_name': request.args.get('last_name', '').strip(),
            'email': request.args.get('email', '').strip(),
            'job_title': request.args.get('job_title', '').strip(),
            'company': request.args.get('company', '').strip(),
            'location': request.args.get('location', '').strip(),
            'role': request.args.get('role', '').strip(),
            'status': request.args.get('status', '').strip()
        }

        # Sorting parameters
        sort = request.args.get('sort', 'id')  # Default sort by ID
        order = request.args.get('order', 'asc')  # Default order is ascending

        # Query distinct values for dropdowns
        companies = [c.name for c in Company.query.all()]  # Fetch all company names
        dropdown_locations = [location.name for location in Location.query.all()]  # Location names
        job_titles = (
        db.session.query(JobTitle.name)
    .join(User, User.job_title_id == JobTitle.id)
    .distinct()
    .all()
)
  # Distinct job titles
        job_titles.sort()  # Sort alphabetically
        all_roles = ['User', 'Admin', 'Sub Admin', 'Security']
        roles = list(set(all_roles + [r[0] for r in db.session.query(User.role).distinct()]))
        roles.sort()

        # Query the database with filters
        query = User.query
        if filters['id']:
            query = query.filter(User.id == filters['id'])
        if filters['first_name']:
            query = query.filter(User.first_name.ilike(f"%{filters['first_name']}%"))
        if filters['last_name']:
            query = query.filter(User.last_name.ilike(f"%{filters['last_name']}%"))
        if filters['email']:
            query = query.filter(User.email.ilike(f"%{filters['email']}%"))
        if filters['job_title']:
            query = query.filter(User.job_title.ilike(f"%{filters['job_title']}%"))
        if filters['company']:
            company = Company.query.filter_by(name=filters['company']).first()
            if company:
                query = query.filter(User.company_id == company.id)
        if filters['location']:
            query = query.join(User.locations).filter(Location.name.ilike(f"%{filters['location']}%"))
        if filters['role']:
            query = query.filter(User.role == filters['role'])
        if filters['status']:
            query = query.filter(User.status == filters['status'])

        # Apply sorting
        if sort == 'id':
            query = query.order_by(User.id.desc() if order == 'desc' else User.id.asc())
        elif sort == 'first_name':
            query = query.order_by(User.first_name.desc() if order == 'desc' else User.first_name.asc())
        elif sort == 'last_name':
            query = query.order_by(User.last_name.desc() if order == 'desc' else User.last_name.asc())
        elif sort == 'email':
            query = query.order_by(User.email.desc() if order == 'desc' else User.email.asc())
        elif sort == 'job_title':
         query = query.order_by(User.job_title_id.desc() if order == 'desc' else User.job_title_id.asc())

        elif sort == 'company':
            query = query.order_by(User.company_id.desc() if order == 'desc' else User.company_id.asc())
        elif sort == 'status':
            query = query.order_by(User.status.desc() if order == 'desc' else User.status.asc())

        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        users = pagination.items

        # Prepare data for template
        user_data = []
        for user in users:
            # Get user locations
            locations = [location.name for location in user.locations]
            location_str = ", ".join(locations)

            # Get company name
            company_name = None  # Default to None if no company is assigned
            if user.company_id:  # Check if the user has a company assigned
                company = Company.query.get(user.company_id)  # Fetch the company object
                company_name = company.name if company else None  # Extract the name if company exists

            # Append user data to the list
            user_data.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'job_title': user.job_title.name if user.job_title else None,
                'company': company_name,
                'locations': location_str,
                'role': user.role,
                'status': user.status
            })

        # Render the template
        return render_template(
            'admin_dashboard.html',
            users=user_data,
            filters=filters,
            companies=companies,
            locations=dropdown_locations,
            job_titles=job_titles,
            roles=roles,
            pagination=pagination,
            sort=sort,
            order=order
        )
    except Exception as e:
        current_app.logger.error(f"Error in admin_dashboard: {e}")
        return "An error occurred while loading the admin dashboard.", 500




# Qualifications Page
@main.route('/qualifications', methods=['GET'])
def qualifications():
    # Fetch all qualifications from the database
    qualifications = Qualification.query.all()
    
    # Render template with qualifications data
    return render_template('qualifications.html', qualifications=qualifications)


@main.route('/qualifications/add', methods=['GET', 'POST'])
def add_qualification():
    if request.method == 'POST':
        qualification_name = request.form.get('qualification_name')
        description = request.form.get('description')
        valid_days = request.form.get('valid_days')

        # Validate mandatory field
        if not qualification_name:
            flash('Qualification Name is required.', 'danger')
            return redirect(url_for('main.add_qualification'))

        # Create a new qualification
        new_qualification = Qualification(
            name=qualification_name,
            description=description,
            valid_days=int(valid_days) if valid_days else None
        )

        # Add to DB
        db.session.add(new_qualification)
        db.session.commit()
        flash('Qualification added successfully!', 'success')
        return redirect(url_for('main.qualifications'))

    return render_template('add_qualification.html')

@main.route('/qualifications/edit/<int:id>', methods=['GET', 'POST'])
def edit_qualification(id):
    qualification = Qualification.query.get_or_404(id)
    if request.method == 'POST':
        qualification.name = request.form['name']
        qualification.description = request.form['description']
        qualification.valid_days = request.form['valid_days']
        db.session.commit()
        flash('Qualification updated successfully!', 'success')
        return redirect(url_for('main.qualifications'))
    return render_template('edit_qualification.html', qualification=qualification)

@main.route('/qualifications/delete/<int:id>', methods=['POST'])
def delete_qualification(id):
    qualification = Qualification.query.get_or_404(id)
    # Check if qualification is assigned to users (dummy check for now)
    assigned_users = False  # Replace with actual check later
    if assigned_users:
        flash('Cannot delete qualification because it is assigned to users.', 'danger')
        return redirect(url_for('main.qualifications'))
    db.session.delete(qualification)
    db.session.commit()
    flash('Qualification deleted successfully!', 'success')
    return redirect(url_for('main.qualifications'))


# Edit User Route
# Edit User Route
# Edit User Route
@main.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    # Fetch user data based on ID
    user = User.query.get_or_404(id)

    # Fetch dropdown options dynamically from the database
    companies = Company.query.all()  # Fetch all companies
    locations = Location.query.all()  # Fetch all locations
    job_titles = JobTitle.query.all()  # Fetch all job titles
    all_roles = ['User', 'Admin', 'Sub Admin', 'Security']
    roles = list(set(all_roles + [r[0] for r in db.session.query(User.role).distinct()]))
    roles.sort()
    statuses = ['Active', 'Inactive']  # Static status options

    if request.method == 'POST':
        # Update user details
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        user.company_id = request.form.get('company_id')  # Store the selected company ID
        user.role = request.form['role']
        user.status = request.form['status']
        user.job_title_id = request.form.get('job_title_id')  # Store the selected Job Title ID

        # Handle locations (many-to-many)
        selected_location_ids = request.form.getlist('locations')  # Get all selected location IDs
        user.locations = []  # Clear current locations
        for location_id in selected_location_ids:
            location = Location.query.get(location_id)
            if location:
                user.locations.append(location)  # Add selected locations

        # Commit changes to the database
        try:
            db.session.commit()
            flash('User updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {e}', 'danger')

        return redirect(url_for('main.admin_dashboard'))

    # Render the template with dropdown data
    return render_template(
        'edit_user.html',
        user=user,
        companies=companies,
        locations=locations,
        job_titles=job_titles,  # Pass job titles to the template
        roles=roles,
        statuses=statuses
    )



# Delete User Route
@main.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    # Check if the user can be deleted (Add custom logic if needed)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('main.admin_dashboard'))

@main.route('/reset_password/<int:id>', methods=['POST'])
def reset_password(id):
    # Fetch the user from the database
    user = User.query.get_or_404(id)

    # Reset the password to 'Password'
    user.password = generate_password_hash('Password')

    # Commit the changes
    db.session.commit()

    # Flash a success message
    flash(f"Password has been reset to 'Password' for {user.first_name} {user.last_name}.", 'success')

    # Redirect back to the admin dashboard
    return redirect(url_for('main.admin_dashboard'))

@main.route('/locations', methods=['GET'])
def view_locations():
    locations = Location.query.all()
    return jsonify([{'id': loc.id, 'name': loc.name} for loc in locations])

@main.route('/add_location/<int:user_id>', methods=['GET', 'POST'])
def add_location(user_id):
    # Retrieve the user by ID
    user = User.query.get_or_404(user_id)

    # Get all available locations
    locations = Location.query.all()

    # Handle form submission
    if request.method == 'POST':
        # Retrieve and validate location ID
        location_id = request.form.get('location_id')

        # Check if location_id is valid
        if not location_id:
            flash('Invalid location selected.', 'danger')
            return redirect(url_for('main.add_location', user_id=user.id))

        location = Location.query.get(location_id)

        # Check if the location exists
        if not location:
            flash('Location not found.', 'danger')
            return redirect(url_for('main.add_location', user_id=user.id))

        # Check if the location is already assigned to the user
        if location not in user.locations:
            # Add location and save to DB
            user.locations.append(location)
            db.session.commit()
            flash('Location added successfully!', 'success')
        else:
            flash('Location already assigned to this user.', 'warning')

        # Redirect back to the admin dashboard
        return redirect(url_for('main.dashboard'))

    # Render the template for the form
    return render_template('add_location.html', user=user, locations=locations)

# Settings Route
# Settings Route
@main.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user_id' not in session or session.get('role') != 'Admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main.home'))

    # Fetch necessary data for dropdowns
    companies = Company.query.all()  # Fetch all companies for dropdown
    roles = ['User', 'Admin', 'Sub Admin', 'Security']  # Predefined roles
    locations = Location.query.all()  # Fetch all locations for dropdown

    if request.method == 'POST':
        flash('Settings updated successfully!', 'success')

    # Render the settings template with all necessary data
    return render_template(
        'settings.html', 
        companies=companies, 
        roles=roles, 
        locations=locations
    )

# Allowed file extensions
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

# Helper function to check if the file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




# Route to create a single company
@main.route('/create_company', methods=['POST'])
def create_company():
    # Get the company name from the form
    company_name = request.form.get('company_name')

    # Validate input
    if not company_name:
        flash('Company name is required!', 'danger')
        return redirect(url_for('main.settings'))

    # Check if company already exists in the Company table
    existing_company = db.session.query(Company).filter_by(name=company_name).first()
    if existing_company:
        flash('Company already exists!', 'warning')
        return redirect(url_for('main.settings'))

    # Add the new company to the Company table
    new_company = Company(name=company_name)
    try:
        db.session.add(new_company)
        db.session.commit()
        flash(f'Company "{company_name}" added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding company: {str(e)}', 'danger')

    return redirect(url_for('main.settings'))


# Route for bulk uploading companies from Excel

# Allowed file extensions for bulk upload
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route for bulk uploading companies from Excel
# Allowed file extensions
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

# Helper function for allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/bulk_upload_companies', methods=['POST'])
def bulk_upload_companies():
    logging.debug("Bulk upload endpoint hit")

    # Check if file is part of the request
    if 'file' not in request.files:
        logging.debug("No file in request")
        flash('No file selected!', 'danger')
        return redirect(url_for('main.settings'))

    file = request.files['file']
    logging.debug(f"Received file: {file.filename}")

    # Validate file selection
    if file.filename == '':
        logging.debug("No file selected")
        flash('No file selected!', 'danger')
        return redirect(url_for('main.settings'))

    # Check if file is valid
    if file and allowed_file(file.filename):
        # Ensure 'uploads' directory exists
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            logging.debug("Creating 'uploads' folder")
            os.makedirs(upload_folder)  # Create folder if it doesn't exist

        # Secure the file name and save temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, filename)
        logging.debug(f"Saving file to: {filepath}")

        file.save(filepath)

        try:
            # Read the Excel file
            logging.debug("Reading Excel file")
            data = pd.read_excel(filepath)
            logging.debug(f"Excel data read: {data.head()}")

            # Check if 'Company' column exists
            if 'Company' not in data.columns:
                logging.debug("Invalid Excel format - 'Company' column missing")
                flash('Invalid Excel format! Missing "Company" column.', 'danger')
                return redirect(url_for('main.settings'))

            # Add companies to the database
            added_count = 0
            for company_name in data['Company']:
                # Trim whitespace and validate
                company_name = str(company_name).strip()
                if not company_name:
                    continue

                # Check if the company already exists
                existing_company = db.session.query(Company).filter_by(name=company_name).first()
                if not existing_company:
                    new_company = Company(name=company_name)
                    db.session.add(new_company)
                    added_count += 1

            # Commit changes
            db.session.commit()
            logging.debug(f"Added {added_count} companies to the database")
            flash(f'{added_count} companies uploaded successfully!', 'success')

        except Exception as e:
            db.session.rollback()
            logging.debug(f"Error processing file: {str(e)}")
            flash(f'Error processing file: {str(e)}', 'danger')

        finally:
            # Remove the uploaded file after processing
            logging.debug("Removing uploaded file")
            os.remove(filepath)

    else:
        logging.debug("Invalid file type")
        flash('Invalid file type! Please upload an Excel file.', 'danger')

    logging.debug("Redirecting to settings")
    return redirect(url_for('main.settings'))

@main.route('/create_location', methods=['POST'])
def create_location():
    # Get location name from the form
    location_name = request.form.get('location_name')
    print(f"Location name received: {location_name}")  # Debugging

    # Check if the location name is provided
    if not location_name:
        flash('Location name is required!', 'danger')
        return redirect(url_for('main.settings'))

    # Check if the location already exists in the database
    existing_location = Location.query.filter_by(name=location_name).first()
    print(f"Existing location: {existing_location}")  # Debugging

    if existing_location:
        flash(f'Location "{location_name}" already exists!', 'warning')
        return redirect(url_for('main.settings'))

    # Create a new location
    new_location = Location(name=location_name)
    try:
        db.session.add(new_location)
        db.session.commit()
        print("Location successfully added to database")  # Debugging
        flash(f'Location "{location_name}" added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")  # Debugging
        flash(f'Error adding location: {str(e)}', 'danger')

    return redirect(url_for('main.settings'))





@main.route('/bulk_upload_locations', methods=['POST'])
def bulk_upload_locations():
    if 'file' not in request.files:
        flash('No file selected!', 'danger')
        return redirect(url_for('main.settings'))

    file = request.files['file']

    if file.filename == '':
        flash('No file selected!', 'danger')
        return redirect(url_for('main.settings'))

    # Check if the file is allowed
    if file and allowed_file(file.filename):
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Save the file
        filepath = os.path.join(upload_folder, secure_filename(file.filename))
        file.save(filepath)

        try:
            # Read the Excel file
            data = pd.read_excel(filepath)

            # Check if the 'Location' column exists
            if 'Location' not in data.columns:
                flash('Invalid Excel format! Missing "Location" column.', 'danger')
                return redirect(url_for('main.settings'))

            # Process each location
            added_count = 0
            for location_name in data['Location']:
                location_name = str(location_name).strip()
                if location_name:
                    existing_location = Location.query.filter_by(name=location_name).first()
                    if not existing_location:
                        new_location = Location(name=location_name)
                        db.session.add(new_location)
                        added_count += 1

            db.session.commit()
            flash(f'{added_count} locations uploaded successfully!', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f'Error processing file: {str(e)}', 'danger')

        finally:
            os.remove(filepath)

    else:
        flash('Invalid file type! Please upload an Excel file.', 'danger')

    return redirect(url_for('main.settings'))



@main.route('/download_company_template', methods=['GET'])
def download_company_template():
    return send_from_directory(
        directory='static/templates', 
        path='bulk_upload_company.xlsx',
        as_attachment=True
    )



@main.route('/download_location_template', methods=['GET'])
def download_location_template():
    try:
        return send_from_directory(
            directory='static/templates',
            path='bulk_upload_location.xlsx',
            as_attachment=True
        )
    except Exception as e:
        flash(f"Error downloading location template: {e}", "danger")
        return redirect(url_for('main.settings'))

from werkzeug.security import generate_password_hash

@main.route('/create_user', methods=['POST'])
def create_user():
    try:
        # Extract form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        company_id = request.form['company_id']
        role = request.form['role']
        location_id = request.form['location_id']  # Assuming it's single-location for now

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash(f'User with email {email} already exists!', 'warning')
            return redirect(url_for('main.settings'))

        # Hash the password
        hashed_password = generate_password_hash('Password123', method='pbkdf2:sha256')

        # Create a new user
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            company_id=company_id,
            role=role,
            status='Active'
        )

        # Add user to database
        db.session.add(new_user)
        db.session.commit()

        # Assign location if applicable (handling many-to-many relationships if needed)
        if location_id:
            location = Location.query.get(location_id)
            if location:
                new_user.locations.append(location)
                db.session.commit()

        flash('User created successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating user: {str(e)}', 'danger')

    return redirect(url_for('main.settings'))

@main.route('/download_user_template', methods=['GET'])
def download_user_template():
    try:
        return send_from_directory(
            directory='static/templates',
            path='bulk_upload_user.xlsx',
            as_attachment=True
        )
    except Exception as e:
        flash(f"Error downloading user template: {str(e)}", 'danger')
        return redirect(url_for('main.settings'))



@main.route('/bulk_upload_users', methods=['POST'])
def bulk_upload_users():
    file = request.files.get('file')
    if not file or not allowed_file(file.filename):
        flash("Invalid file format. Please upload an Excel file.", "danger")
        return redirect(url_for('main.settings'))

    filename = secure_filename(file.filename)
    file_path = os.path.join('uploads', filename)
    file.save(file_path)

    try:
        # Read the Excel file
        data = pd.read_excel(file_path)

        # Validate the required columns
        required_columns = ['First Name', 'Last Name', 'Email', 'Company', 'Role', 'Location']
        if not all(column in data.columns for column in required_columns):
            flash("Invalid template. Ensure the file has all required columns.", "danger")
            return redirect(url_for('main.settings'))

        # Process each row
        for index, row in data.iterrows():
            try:
                # Extract row data
                first_name = row['First Name']
                last_name = row['Last Name']
                email = row['Email']
                company_name = row['Company']
                role = row['Role']
                location_name = row['Location']

                # Validate email
                if User.query.filter_by(email=email).first():
                    flash(f"Row {index + 1}: Email {email} already exists. Skipped.", "warning")
                    continue

                # Find company
                company = Company.query.filter_by(name=company_name).first()
                if not company:
                    flash(f"Row {index + 1}: Company {company_name} not found. Skipped.", "warning")
                    continue

                # Find location
                location = Location.query.filter_by(name=location_name).first()
                if not location:
                    flash(f"Row {index + 1}: Location {location_name} not found. Skipped.", "warning")
                    continue

                # Hash the password
                hashed_password = generate_password_hash('Password123', method='pbkdf2:sha256')

                # Create user
                new_user = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=hashed_password,
                    company_id=company.id,
                    role=role,
                    status='Active'
                )
                db.session.add(new_user)
                db.session.commit()

                # Assign location
                new_user.locations.append(location)
                db.session.commit()

                flash(f"Row {index + 1}: User {email} created successfully.", "success")

            except Exception as row_error:
                flash(f"Row {index + 1}: Error processing row: {str(row_error)}", "danger")

    except Exception as e:
        flash(f"Error processing file: {str(e)}", "danger")
    finally:
        # Remove the uploaded file
        os.remove(file_path)

    return redirect(url_for('main.settings'))

@main.route('/content', methods=['GET'])
def content():
    if 'user_id' not in session or session.get('role') != 'Admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main.home'))

    return render_template('content.html')

@main.route('/modules', methods=['GET'])
def modules():
    if 'user_id' not in session or session.get('role') != 'Admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main.home'))

    # Query all modules from the database
    modules = Module.query.all()

    return render_template('modules.html', modules=modules)

# Utility function to check allowed file types
def allowed_file(filename):
    """
    Checks if the file has an allowed extension.
    This function accepts files with a .zip extension.

    Args:
        filename (str): Name of the file being uploaded.

    Returns:
        bool: True if the file is allowed, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'zip'}

@main.route('/add_module_placeholder', methods=['GET', 'POST'])
def add_module_placeholder():
    if request.method == 'POST':
        # Check if the file exists in the request
        if 'scorm_file' not in request.files:
            flash("No file part in the request", "danger")
            print("DEBUG: No file part in the request")
            return redirect(request.url)

        file = request.files['scorm_file']
        if file.filename == '':
            flash("No selected file", "danger")
            print("DEBUG: No file selected")
            return redirect(request.url)

        if allowed_file(file.filename):
            # Define paths
            scorm_folder = os.path.join(current_app.static_folder, 'scorm_uploads')
            os.makedirs(scorm_folder, exist_ok=True)

            # Save the uploaded ZIP file
            zip_path = os.path.join(scorm_folder, secure_filename(file.filename))
            file.save(zip_path)
            print(f"DEBUG: File saved to {zip_path}")

            # Unpack the ZIP file
            extract_path = os.path.join(scorm_folder, os.path.splitext(file.filename)[0])
            os.makedirs(extract_path, exist_ok=True)

            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                print(f"DEBUG: File extracted to {extract_path}")

                # Validate SCORM package
                manifest_path = os.path.join(extract_path, 'imsmanifest.xml')
                if not os.path.exists(manifest_path):
                    flash("Invalid SCORM package: Missing imsmanifest.xml.", "danger")
                    print("DEBUG: imsmanifest.xml not found")
                    return redirect(request.url)

                # Parse and validate imsmanifest.xml
                try:
                    # Update namespace based on the actual manifest
                    namespaces = {'default': 'http://www.imsproject.org/xsd/imscp_rootv1p1p2'}
                    tree = etree.parse(manifest_path)
                    root = tree.getroot()

                    # Debugging: Print XML content
                    print("DEBUG: imsmanifest.xml Content")
                    print(etree.tostring(root, pretty_print=True).decode())

                    # Find the title element
                    title_element = root.find(".//default:title", namespaces)
                    if title_element is None or title_element.text is None:
                        flash("Invalid SCORM package: Missing or invalid title in imsmanifest.xml.", "danger")
                        print("DEBUG: Missing or invalid title in imsmanifest.xml")
                        return redirect(request.url)

                    title = title_element.text
                    print(f"DEBUG: SCORM Title: {title}")

                    # Save module to database
                    module = Module(name=title, file_name=os.path.splitext(file.filename)[0])
                    db.session.add(module)
                    db.session.commit()
                    print("DEBUG: Module saved to database")
                    flash(f"SCORM Module '{title}' uploaded and validated successfully!", "success")
                    return redirect(url_for('main.modules'))
                except Exception as e:
                    flash(f"Invalid imsmanifest.xml: {e}", "danger")
                    print(f"DEBUG: imsmanifest.xml parsing error: {e}")
                    return redirect(request.url)

            except zipfile.BadZipFile:
                flash("Uploaded file is not a valid ZIP file.", "danger")
                print("DEBUG: Bad ZIP file")
                return redirect(request.url)
        else:
            flash("Invalid file type. Please upload a valid SCORM ZIP file.", "danger")
            print("DEBUG: Invalid file type")
            return redirect(request.url)

    return render_template('add_module_placeholder.html')



# Allowed file helper function
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'zip'}



@main.route('/launch_scorm/<int:module_id>', methods=['GET'])
def launch_scorm(module_id):
    # Fetch the module from the database
    module = Module.query.get_or_404(module_id)

    # Construct the path to the SCORM content
    scorm_path = f'scorm_uploads/{module.file_name}/scormcontent/index.html'

    # Pass the module and the SCORM file path to the template
    return render_template('scorm_launch.html', module=module, scorm_file=scorm_path)



@main.route('/delete_module/<int:module_id>', methods=['GET', 'POST'])
def delete_module(module_id):
    # Query the module by its ID
    module = Module.query.get_or_404(module_id)

    try:
        # Define the path to the SCORM folder
        scorm_folder = os.path.join(current_app.static_folder, 'scorm_uploads', module.file_name)

        # Delete the SCORM folder if it exists
        if os.path.exists(scorm_folder):
            import shutil
            shutil.rmtree(scorm_folder)

        # Delete the module from the database
        db.session.delete(module)
        db.session.commit()

        flash(f"Module '{module.name}' has been deleted successfully.", "success")
    except Exception as e:
        flash(f"An error occurred while deleting the module: {e}", "danger")

    # Redirect back to the modules page
    return redirect(url_for('main.modules'))

@main.route('/settings/job_titles', methods=['GET', 'POST'])
def manage_job_titles():
    try:
        if request.method == 'POST':
            job_title_name = request.form.get('job_title_name').strip()
            if job_title_name:
                # Check if the job title already exists
                existing_job_title = JobTitle.query.filter_by(name=job_title_name).first()
                if existing_job_title:
                    flash('Job title already exists.', 'warning')
                else:
                    # Add the new job title
                    new_job_title = JobTitle(name=job_title_name)
                    db.session.add(new_job_title)
                    db.session.commit()
                    flash('Job title added successfully!', 'success')
        # Fetch all job titles for display
        job_titles = JobTitle.query.all()
        return render_template('settings.html', job_titles=job_titles)
    except Exception as e:
        current_app.logger.error(f"Error managing job titles: {e}")
        flash('An error occurred while managing job titles.', 'danger')
        return redirect(url_for('main.settings'))



@main.route('/settings/upload_job_titles', methods=['POST'])
def upload_job_titles():
    try:
        file = request.files['file']
        if file:
            df = pd.read_excel(file)  # Assuming the file is an Excel file
            for _, row in df.iterrows():
                job_title_name = row['Job Title']
                if job_title_name:
                    # Check if job title already exists
                    existing_job_title = JobTitle.query.filter_by(name=job_title_name).first()
                    if not existing_job_title:
                        new_job_title = JobTitle(name=job_title_name)
                        db.session.add(new_job_title)
            db.session.commit()
            flash('Job titles uploaded successfully!', 'success')
        else:
            flash('No file uploaded.', 'warning')
    except Exception as e:
        current_app.logger.error(f"Error uploading job titles: {e}")
        flash('An error occurred while uploading job titles.', 'danger')
    return redirect(url_for('main.settings'))

@main.route('/download_job_title_template', methods=['GET'])
def download_job_title_template():
    # Correct path to the job title template file
    template_path = os.path.join(current_app.root_path, 'static', 'templates', 'job_title_template.xlsx')
    try:
        return send_from_directory(
            directory=os.path.dirname(template_path),
            path=os.path.basename(template_path),
            as_attachment=True
        )
    except FileNotFoundError:
        flash("Template file not found.", "danger")
        return redirect(url_for('main.settings'))


