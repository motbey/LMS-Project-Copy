from flask import render_template, redirect, url_for, flash, request, session
from werkzeug.security import check_password_hash
from . import auth
from database import db
from ..models import User

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            session['email'] = user.email
            session['role'] = user.role
            return redirect(url_for('main.home'))
        
        flash('Invalid email or password', 'danger')
    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('main.home'))
  