from flask import Flask
from flask_cors import CORS
from config import *
from routes.hello_world_route import hello_world
from routes import hello_world, point_cloud_routes, slicing_routes

app = Flask(__name__)
CORS(app, origins=[WEBSITE_SERVER])

# Register routes
app.register_blueprint(hello_world)
# Register the point cloud and slicing routes
app.register_blueprint(point_cloud_routes)
app.register_blueprint(slicing_routes)

if __name__ == "__main__":
    app.run(debug=True, port=BACKEND_PORT)
