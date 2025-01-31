"""
Module for handling authentication routes in TaskFlow 2.0 app.

Routes:
    - GET /login: Renders login page,
        redirects if already authenticated.
    - POST /login: Processes login form, checks credentials.
    - GET /logout: Logs the user out and redirects to login.
    - GET /signup: Renders sign-up page, redirects if already authenticated.
    - POST /signup: Processes sign-up form, validates data, creates user.
    - GET /terms: Renders terms and conditions page
"""
from flask import (Blueprint, render_template, request,
                   flash, redirect, url_for)
from flask_login import login_user, login_required, logout_user, current_user
from ..models.user import User


# Define auth blueprint
auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """ Logs the user in. """
    # If current user is authenticated, redirect to dashboard page
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # If the request method is POST, process the login form submission
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Check if 'remember_me' is in the form (if checked)
        remember_me = 'remember_me' in request.form

        # Check if all credentials are provided.
        if not email or not password:
            flash('Please fill in all credentials.', 'error')
            return render_template('auth/login.html')

        # Check if the user exists by looking up the email
        user = User.query.filter_by(email=email).first()
        # If password matches, login the user
        if user and user.check_password(password):
            flash('Logged in successfully!', 'success')
            # Check if remember me is checked
            if remember_me:
                login_user(user, remember=True)
            else:
                login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            # Flash error if the password is incorrect
            # or user doesn't exist
            flash("Invalid login credentials. Please try again.", 'error')

    # Render the login page with the current user context
    return render_template('auth/login.html')


@auth_blueprint.route('/logout')
@login_required
def logout():
    """ Logs the user out. """
    # Log the user out and clear the session
    logout_user()
    # Flash a success message indicating the user has been logged out
    flash('You have logged out successfully.', 'sucess')
    return render_template('auth/login.html')


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def sign_up():
    """ Signs the user up. """
    # If current user is authenticated, redirect to dashboard page
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # If the request method is POST, process the login form submission
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        auto_login_on_signup = 'auto_login_on_signup' in request.form

        # Check if all credentials are provided.
        if not email or not name or not password or not confirm_password:
            flash('Please fill in all credentials.', 'error')
            return render_template('auth/signup.html',
                                   email=email,
                                   name=name)

        # Check if the user exists by looking up the email
        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email is already associated with another account.',
                  'error')
            return render_template('auth/signup.html',
                                   email=email,
                                   name=name)

        # Validate credentials.
        elif len(name) < 1 or len(name) > 20:
            flash("Name must be between 1 and 20 characters.", 'error')
        elif len(password) < 6:
            flash("Password must be at least 6 characters.", 'error')
        elif confirm_password != password:
            flash("Passwords don't match.", 'error')
        else:
            new_user = User(
                email=email,
                name=name,
                password=password,
            )

            # Set the password using a setter method or similar
            new_user.set_password(password)
            # Save user in the database
            new_user.save()
            flash("Account created successfully!", 'success')

            # Check if auto login on signup is checked
            if auto_login_on_signup:
                login_user(new_user, remember=True)
                return redirect(url_for('main.dashboard'))
            else:
                return render_template('auth/login.html')

    # if the method is GET Render the sign-up page
    return render_template('auth/signup.html', user=current_user)


@auth_blueprint.route('/terms')
def terms():
    """ Loads terms and conditions page. """
    return render_template('auth/terms.html')
