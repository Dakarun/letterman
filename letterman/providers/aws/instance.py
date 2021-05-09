from letterman.utils.helpers import flatten_dict
from letterman.providers.base.instance import Instance
from letterman.providers.aws.utils import get_ec2_client


class EC2Instance(Instance):
    def __init__(self, response):
        super().__init__(response)

    async def start(self) -> dict:
        client = get_ec2_client()
        if self.get_instance_state == 'running':
            return {'success': False, 'msg': 'Server is already running'}
        else:
            instances = client.start_instances(InstanceIds=[self.get_instance_id])
            self.update_properties(instances)

    async def stop(self) -> dict:
        client = get_ec2_client()
        waiter = client.get_waiter('instance_stopped')
        instances = client.stop_instances(InstanceIds=[self.get_instance_id])
        waiter.wait(InstanceIds=[instance['InstanceId'] for instance in instances['StoppingInstances']])
        self.update_properties(instances)
        return {'success': True, 'resource': self.get_instance_id, 'msg': 'Instance successfully stopped'}

    async def create(self, **kwargs):
        client = get_ec2_client()
        client.run_instances(**kwargs)
        waiter = client.get_waiter('instance_running')
        instances = client.run_instances(InstanceIds=[self.get_instance_id])
        waiter.wait(InstanceIds=[instance['InstanceId'] for instance in instances['Instances']])
        self.update_properties(instances)

    async def destroy(self) -> None:
        client = get_ec2_client()
        waiter = client.get_waiter('instance_stopped')
        instances = client.termiante_instances(InstanceIds=[self.get_instance_id])
        waiter.wait(InstanceIds=[instance['InstanceId'] for instance in instances['Instances']])
        self.update_properties(instances)

    def _generate_instance_tags(self) -> dict:
        return {'Name': self.get_name, 'game': self.get_game}

    def _generate_instance_filter(self) -> list:
        default_tags = self._generate_instance_tags()
        return [{'Name': 'tag:{}'.format(key), 'Values': [value]} for key, value in default_tags]

    def _parse_api_response(self, response: dict) -> dict:
        # TODO: Automatically pull Instances key from nesting
        if response.get("InstanceId"):
            instance = response
        elif not response.get("Instances"):
            raise Exception(f"No instances in response dict: {response}")
        elif len(response.get("Instances")) > 1:
            raise Exception(f"More than one instance in response dict: {response}")
        else:
            instance = response.get("Instances")[0]

        root_keys_map = {
            "id": "InstanceId",
            "image": "ImageId",
            "state": "State.Name",
            "public_ip": "PublicIpAddress",
        }

        flattened_instance = flatten_dict(instance, ".")
        response_properties = {}
        for key, value in root_keys_map:
            response_properties[key] = flattened_instance[value]
        return response_properties
