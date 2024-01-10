# routes.py
from time import sleep
from sqlalchemy.exc import OperationalError
from flask import Flask, render_template, request
from flask_restx import Api, Resource, fields
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
import os
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)

def create_app():
    app = Flask(__name__)

    # Use SQLite as default if no DATABASE_URL is provided
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///exercises.db')
    logging.info(database_url)

    # Configure the database connection
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db = SQLAlchemy(app)

    # Create a Blueprint
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp, version='1.0', doc='/api', title='Sample API', description='A simple API', prefix='/api')


    # Define the model for Body Measurements
    body_measurement_model = api.model('BodyMeasurement', {
        'id': fields.Integer(readonly=True),
        'date': fields.DateTime(required=True, description='Date of measurement'),
        'biceps': fields.Float(description='Biceps size in inches'),
        'waist': fields.Float(description='Waist size in inches'),
        'shoulders': fields.Float(description='Shoulders size in inches'),
        'chest': fields.Float(description='Chest size in inches'),
        'calves': fields.Float(description='Calves size in inches')
    })

    exercise_model = api.model('Exercise', {
        'id': fields.Integer(readonly=True),
        'date': fields.DateTime(required=True, description='Date of weight entry'),
        'exercise': fields.String(required=True, description='The exercise name'),
        'sets': fields.Integer(required=True, description='Number of sets'),
        'reps': fields.Integer(required=True, description='Number of reps')
    })

    weight_model = api.model('Weight', {
        'id': fields.Integer(readonly=True),
        'date': fields.DateTime(required=True, description='Date of weight entry'),
        'weight': fields.Float(required=True, description='Weight in kilograms')
    })

    sleep_model = api.model('Sleep', {
        'id': fields.Integer(readonly=True),
        'date': fields.DateTime(required=True, description='Date of sleep entry'),
        'hours': fields.Float(required=True, description='Number of hours slept')
    })

    heart_model = api.model('Heart', {
        'id': fields.Integer(readonly=True),
        'date': fields.DateTime(required=True, description='Date of heart rate entry'),
        'rate': fields.Integer(required=True, description='Heart rate in beats per minute')
    })

    blog_model = api.model('Blog', {
        'id': fields.Integer(readonly=True),
        'date': fields.DateTime(required=True, description='Date of the blog entry'),
        'title': fields.String(required=True, description='Blog title'),
        'content': fields.String(required=True, description='Blog content')
    })

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



    # Use app.app_context() to create an application context
    with app.app_context():
        # Retry connecting to the database for a certain number of attempts
        max_attempts = 10
        for attempt in range(max_attempts):
            try:
                # Attempt to create the database connection
                db.create_all()
                break  # If successful, break out of the loop
            except OperationalError as e:
                logging.info(f"Attempt {attempt + 1}/{max_attempts}: Unable to connect to the database. Retrying...")
                sleep(5)  # Wait for 5 seconds before retrying

    @api.route('/hello')
    class HelloResource(Resource):
        def get(self):
            """Returns a simple greeting"""
            logging.info(database_url)
            logging.info("Hello!!!!")
            return {'message': 'Hello, World!'}

    @api.route('/exercises')
    class ExercisesResource(Resource):
        @api.marshal_with(exercise_model, as_list=True)
        def get(self):
            """Returns a list of all exercises"""
            exercises = Exercise.query.all()
            return exercises

        @api.expect(exercise_model)
        def post(self):
            """Add a new exercise"""
            date_str = request.json['date']
            date_object = datetime.fromisoformat(date_str)
            new_exercise = Exercise(
                date=date_object,
                exercise=request.json['exercise'],
                sets=request.json['sets'],
                reps=request.json['reps']
            )
            db.session.add(new_exercise)
            db.session.commit()
            return {'message': 'Exercise added successfully'}, 201

    @api.route('/weight')
    class WeightResource(Resource):
        @api.marshal_with(weight_model, as_list=True)
        def get(self):
            """Returns a list of all weight entries"""
            weight = Weight.query.all()
            return weight

        @api.expect(weight_model)
        def post(self):
            """Add a new weight entry"""
            new_weight = Weight(
                date=datetime.fromisoformat(request.json['date']),
                weight=request.json['weight']
            )
            db.session.add(new_weight)
            db.session.commit()
            return {'message': 'Weight entry added successfully'}, 201

    @api.route('/sleep')
    class SleepResource(Resource):
        @api.marshal_with(sleep_model, as_list=True)
        def get(self):
            """Returns a list of all sleep entries"""
            sleeps = Sleep.query.all()
            return sleeps

        @api.expect(sleep_model)
        def post(self):
            """Add a new sleep entry"""
            new_sleep = Sleep(
                date=datetime.fromisoformat(request.json['date']),
                hours=request.json['hours']
            )
            db.session.add(new_sleep)
            db.session.commit()
            return {'message': 'Sleep entry added successfully'}, 201

    @api.route('/heart')
    class HeartResource(Resource):
        @api.marshal_with(heart_model, as_list=True)
        def get(self):
            """Returns a list of all heart rate entries"""
            hearts = Heart.query.all()
            return hearts

        @api.expect(heart_model)
        def post(self):
            """Add a new heart rate entry"""
            new_heart = Heart(
                date=datetime.fromisoformat(request.json['date']),
                rate=request.json['rate']
            )
            db.session.add(new_heart)
            db.session.commit()
            return {'message': 'Heart rate entry added successfully'}, 201

    @api.route('/blog')
    class BlogResource(Resource):
        @api.marshal_with(blog_model, as_list=True)
        def get(self):
            """Returns a list of all blog entries"""
            blogs = Blog.query.all()
            return blogs

        @api.expect(blog_model)
        def post(self):
            """Add a new blog entry"""
            new_blog = Blog(
                date=datetime.fromisoformat(request.json['date']),
                title=request.json['title'],
                content=request.json['content']
            )
            db.session.add(new_blog)
            db.session.commit()
            return {'message': 'Blog entry added successfully'}, 201

    # Add the Body Measurements resource to the API
    @api.route('/body_measurements')
    class BodyMeasurementsResource(Resource):
        @api.marshal_with(body_measurement_model, as_list=True)
        def get(self):
            """Returns a list of all body measurements"""
            body_measurements = BodyMeasurement.query.all()
            return body_measurements

        @api.expect(body_measurement_model)
        def post(self):
            """Add a new body measurement"""
            new_measurement = BodyMeasurement(
                date=datetime.fromisoformat(request.json['date']),
                biceps=request.json.get('biceps'),
                waist=request.json.get('waist'),
                shoulders=request.json.get('shoulders'),
                chest=request.json.get('chest'),
                calves=request.json.get('calves')
            )
            db.session.add(new_measurement)
            db.session.commit()
            return {'message': 'Body measurement added successfully'}, 201

    # UI Routes
    @app.route('/body_measurements', methods=['GET'])
    def body_measurements_ui():
        """Render HTML page for viewing body measurements"""
        measurements = BodyMeasurement.query.all()
        logging.info(measurements)
        return render_template('body_measurements.html', measurements=measurements)

    # UI Routes
    @app.route('/blog', methods=['GET'])
    def blog_ui():
        """Render HTML page for viewing blog entries"""
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)

    return app, db, api_bp