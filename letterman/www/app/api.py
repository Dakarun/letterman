from flask import request
from flask_appbuilder.api import BaseApi, expose, rison, safe
from flask_appbuilder.security.decorators import protect

from letterman.constants import PROVIDER_AWS
from letterman.providers.aws.instance import EC2Instance
from letterman.www.app import app, appbuilder

create_instance_schema = {"type": "object", "propeties": {"name": {"type": "string"}, "game": {"type": "string"}}}

class InstanceAPI(BaseApi):
    version = "v1"
    resource_name = "instances"
    provider = app.config['']
    # apispec_parameter_schemas = {"": ""}

    @expose('/list', methods=['GET'])
    def list(self, **kwargs):
        """List out instances
        ---
        get:
          responses:
            200:
              description: List instances
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      instances:
                        type: array"""
        if 'game' in kwargs['rison']:
            pass
        pass


appbuilder.add_api(InstanceAPI)


class InstanceApi(BaseApi):
    version = "v1"
    resource_name = "instance"
    provider = app.config.get("PROVIDER")
    apispec_parameter_schemas = {"create_instance_schema": create_instance_schema}

    @expose("/create", methods=["POST"])
    def create(self, **kwargs):
        """Create a new instance
        ---
        post:
          parameters:
          - $ref: '#/components/parameters/create_instance_schema'
          responses:
            201:
              description: Create an instance
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
        """
        if self.provider == PROVIDER_AWS:
            instance = EC2Instance(**kwargs)
            await instance.create(**kwargs)
        else:
            raise Exception("No provider configured, please set PROVIDER in your config.py")

    @expose("/destroy", methods=["POST"])
    def destroy(self, instance_id):
        pass

    @expose("/describe", methods=["GET"])
    def describe(self, instance_id):
        pass

    @expose("/start")
    def start(self, instance_id):
        pass

    @expose("/stop")
    def stop(self, instance_id):
        pass


appbuilder.add_api(InstanceAPI)
