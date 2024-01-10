# app.py

from routes import create_app

# Call create_app() to set up the Flask app, database, and API blueprint
app, db, api_bp = create_app()

# Register the API blueprint with the Flask app
app.register_blueprint(api_bp)

# Use app.app_context() to create an application context
with app.app_context():
    # Create the database tables
    db.create_all()

# Function to get a list of all available routes
def get_routes_list():
    routes_list = []
    routes_exluded = ['static','cara','darebeeapi',
                      'update_exclude_file','get_exclude_exercises']
    for rule in app.url_map.iter_rules():
        if rule.endpoint not in routes_exluded:
            routes_list.append(rule.endpoint)

    # Sort the routes alphabetically, but move 'HOME' to the front
    routes_list = sorted(routes_list)

    # Move 'HOME' to the beginning of the list
    if 'home' in routes_list:
        routes_list.remove('home')
        routes_list.insert(0, 'home')

    return routes_list

if __name__ == '__main__':
    routes_list = get_routes_list()
    print(routes_list)
    app.run(debug=True, host="0.0.0.0")
