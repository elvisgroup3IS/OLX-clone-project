"""
This module contains user functions for save to db and search by email.
"""
import models

def save_user(user: models.User) -> None:
    """
    Saves a user to the database.
    """
    models.db.session.add(user)
    models.db.session.commit()

def search_for_user(email: str) -> models.User:
    """
    Searches for a user in the database based on their email.
    """
    return models.User.query.filter_by(email=email).first()