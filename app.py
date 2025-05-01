from flask import Flask
from api.routes.movie_routes import movie_routes

app = Flask(__name__)
app.register_blueprint(movie_routes)


app.run(port=5000,host='0.0.0.0')