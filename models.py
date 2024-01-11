# models.py

from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask
import logging

# Initialize the database
db = SQLAlchemy()


# Define the database models for different endpoints
class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    exercise = db.Column(db.String(100), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)

# Define the database model for Body Measurements
class BodyMeasurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    biceps = db.Column(db.Float)
    waist = db.Column(db.Float)
    shoulders = db.Column(db.Float)
    chest = db.Column(db.Float)
    calves = db.Column(db.Float)

class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    weight = db.Column(db.Float, nullable=False)

class Sleep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    hours = db.Column(db.Float, nullable=False)

class Heart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    rate = db.Column(db.Integer, nullable=False)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)