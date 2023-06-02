
from setuptools import setup, find_packages

setup(
    name='django-simple-notification',
    version='0.0.1',
    description='Simple user notification management for the Django web framework',
    author='Mahmoud Nasser',
    author_email='mahmoud.nasser.abdulhamed@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Django>=3.0',
        'channels>=3.0',
    ],
    include_package_data=True,
    package_data={
        '': ['*.*'],
    },
)
