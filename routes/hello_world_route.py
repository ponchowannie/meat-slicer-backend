from flask import Blueprint

hello_world = Blueprint("hello_world", __name__)

@hello_world.route("/", methods=["GET"])
def index():
    return "Hello World!"
