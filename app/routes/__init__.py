import os
from flask import Flask
from flask_restx import Api as BaseAPI, Resource
from werkzeug.exceptions import BadRequest
from jsonschema import ValidationError
from .tasks import tasks_namespace
from .user import user_namespace

class Api(BaseAPI):
    def _register_doc(self, app_or_blueprint):
        if self._add_specs and self._doc:
            app_or_blueprint.add_url_rule(self._doc, "doc", self.render_doc)

    @property
    def base_path(self):
        return ""

api = Api(
    title="TASK MANAGER API",
    version="1.0",
    description="Rest api for Task Manager project",
    doc="/swagger/",
)

@api.route("/")
class HealthCheck(Resource):
    def get(self):
        return {"status": "OK"}

@api.errorhandler(BadRequest)
def handle_bad_request(error):
    return {"error": str(error)}, 400

@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return {"error": str(error), "message": error.message}, 400

api.add_namespace(tasks_namespace, path="/api/v1/tasks")
api.add_namespace(user_namespace, path='/api/v1/users')