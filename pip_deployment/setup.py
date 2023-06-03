from setuptools import setup, find_packages

setup(
    name='django-simple-notification',
    version='1.0.3',
    author='Mahmoud Nasser',
    author_email='mahmoud.nasser.abdulhamed@gmail.com',
    description='Simple user notification management for the Django web framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MahmoudNasser01/django_simple_notification',
    license='MIT',
    platform='any',
    keywords='django notification simple custom',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'Django>=3.0',
        # Add any other dependencies required by your project
    ],
)
