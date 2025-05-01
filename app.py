from flask import Flask,send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from api.routes.movie_routes import movie_routes

app = Flask(__name__)
app.register_blueprint(movie_routes)


swagger_url = '/swagger'
API_URL = '/static/swagger.yaml'

swagger_blueprint = get_swaggerui_blueprint(swagger_url, API_URL, config={'app_name': 'API Cine AI'})
app.register_blueprint(swagger_blueprint)

swagger_blueprint = get_swaggerui_blueprint(
    swagger_url,
    API_URL,
    config={'app_name':'API Cine AI'}
)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static',path)


app.run(port=5000,host='0.0.0.0')