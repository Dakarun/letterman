from letterman.providers.aws.instance import EC2Instance
from letterman.providers.aws.utils import get_ec2_client
from letterman.providers.base.manager import Manager


class EC2Manager(Manager):
    def list(self):
        pass

    async def list_instances(self, filters) -> list:
        ec2_client = get_ec2_client()
        response = ec2_client.describe_instances(Filters=filters)
        instances = []
        for instance in response.get("Reservations").get("Instances"):
            instances.append(EC2Instance(instance))

    async def list_security_groups(self, filters):
        ec2_client = get_ec2_client()
        return ec2_client.describe_security_groups(Filters=filters)
