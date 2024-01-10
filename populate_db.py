import requests
from datetime import datetime, timedelta
import random

# Set the API base URL
BASE_URL = 'http://127.0.0.1:5000/api'
username = 'laverty'
password = 'laverty'

# Create a function to add dummy blog entries
def add_dummy_blog(title, content):
    blog_data = {
        'date': datetime.utcnow().isoformat(),
        'title': title,
        'content': content
    }
    blog_response = requests.post(f'{BASE_URL}/blog', json=blog_data)
    return blog_response.json()

# Create a function to add dummy body measurements
def add_dummy_body_measurement(date, biceps, waist, shoulders, chest, calves):
    body_measurement_data = {
        'date': date,
        'biceps': biceps,
        'waist': waist,
        'shoulders': shoulders,
        'chest': chest,
        'calves': calves
    }
    body_measurement_response = requests.post(f'{BASE_URL}/body_measurements', json=body_measurement_data)
    return body_measurement_response.json()


# Add dummy exercise, weight, sleep, and heart rate entries (just like before)
for i in range(10):
    # Dummy date for populating the database
    current_date = datetime.utcnow()

    current_date -= timedelta(days=1)  # Subtract one day for each iteration
    exercise_data = {'date': current_date.isoformat(), 'exercise': 'Running', 'sets': 3, 'reps': 10, 'value': random.uniform(5.0, 10.0)}
    requests.post(f'{BASE_URL}/exercises', json=exercise_data)

    weight_data = {'date': current_date.isoformat(), 'weight': 70.5 + random.uniform(-2.0, 2.0)}
    requests.post(f'{BASE_URL}/weight', json=weight_data)

    sleep_data = {'date': current_date.isoformat(), 'hours': 7.5 + random.uniform(-1.0, 1.0)}
    requests.post(f'{BASE_URL}/sleep', json=sleep_data)

    heart_data = {'date': current_date.isoformat(), 'rate': 80 + random.uniform(-5, 5)}
    requests.post(f'{BASE_URL}/heart', json=heart_data)

    # Add dummy body measurements for the new endpoint
    body_measurement_data = {
        'date': current_date.isoformat(),
        'biceps': random.uniform(10.0, 15.0),
        'waist': random.uniform(30.0, 40.0),
        'shoulders': random.uniform(40.0, 50.0),
        'chest': random.uniform(35.0, 45.0),
        'calves': random.uniform(12.0, 18.0)
    }
    requests.post(f'{BASE_URL}/body_measurements', json=body_measurement_data)

# Add 10 dummy blog entries
for i in range(1, 11):
    blog_title = f'Blog {i}'
    blog_content = f'This is dummy blog entry #{i}.'
    add_dummy_blog(blog_title, blog_content)
    print(f'Added blog entry: {blog_title}')

print('Finished adding 10 blog entries and body measurements.')
