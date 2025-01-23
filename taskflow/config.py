"""
Module for TaskFlow configuration.

This module defines the configuration settings for TaskFlow 2.0.
"""

import os


class Config:
    """
    Configuration class for TaskFlow 2.0.

    This class holds all the application settings that configures
    the behavior of TaskFlow.
    """
    # Get database URI.
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', 'mysql://user:password@localhost/taskflow_db')
    # Turn off sql track modifications.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Get secret key.
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    # Define profile pictures upload folder.
    PROFILE_PICS_UPLOAD_FOLDER = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'static', 'profile_pics')
