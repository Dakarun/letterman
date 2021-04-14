from letterman.providers.base.instance import Instance
from letterman.providers.aws.utils import get_ec2_client


class EC2Instance(Instance):
    def __init__(self, name: str, game: str, public_ip=None):
        super().__init__(name, game, public_ip)
        self.name = name
        self.game = game
        self.public_ip = public_ip
        self.instance_id = self._get_instance_id()
        self.instance = None

    @property
    def filters(self):
        return {}

    async def _get_instance(self) -> dict:
        client = get_ec2_client()
        instance = client.describe_instances(InstanceIds=[self._get_instance_id()])['Reservations'][0]
        return instance

    async def _get_instance_id(self) -> str:
        # client = get_ec2_client()
        # instances = client.describe_instances(InstanceIds=[self._get_instance_id()])['Reservations']
        pass

    async def _get_instance_state(self) -> str:
        instance = await self._get_instance()
        return instance.get('State').get('Name')

    async def start(self) -> dict:
        client = get_ec2_client()
        if self._get_instance_state() == 'running':
            return {'success': False, 'msg': 'Server is already running'}
        else:
            client.start_instances(InstanceIds=[self._get_instance_id()])

    async def stop(self) -> dict:
        client = get_ec2_client()
        waiter = client.get_waiter('instance_stopped')
        instances = client.stop_instances(InstanceIds=[self._get_instance_id()])
        waiter.wait(InstanceIds=[instance['InstanceId'] for instance in instances['StoppingInstances']])
        return {'success': True, 'resource': self.instance_id, 'msg': 'Instance successfully stopped'}

    async def get(self):
        pass

    async def create(self, **kwargs):
        client = get_ec2_client()
        client.run_instances(**kwargs)
        waiter = client.get_waiter('instance_running')
        instances = client.run_instances(InstanceIds=[self._get_instance_id()])
        waiter.wait(InstanceIds=[instance['InstanceId'] for instance in instances['Instances']])

    async def destroy(self) -> None:
        client = get_ec2_client()
        waiter = client.get_waiter('instance_stopped')
        client.termiante_instances(InstanceIds=[self._get_instance_id()])

    def _generate_instance_tags(self) -> dict:
        return {'Name': self.name, 'game': self.game}

    def _generate_instance_filter(self) -> list:
        default_tags = self._generate_instance_tags()
        return [{'Name': 'tag:{}'.format(key), 'Values': [value]} for key, value in default_tags]
