from flask import Blueprint, make_response, render_template

error = Blueprint("error", __name__)


@error.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@error.errorhandler(500)
def exception_handler(e):
    error.logger.error(e)
    return make_response("Server Error\n", 500)
