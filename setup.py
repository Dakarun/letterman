from setuptools import setup

version = '0.0.1'
install_requires = [
    'flask-appbuilder==3.2.2',
    'boto3==1.17.50',
]

test_requires = []
setup(
    name='letterman',
    version=version,
    description='Run game servers',
    license="MIT",
    author='@Dakarun',
    packages=['letterman'],
    install_requires=install_requires,
)
