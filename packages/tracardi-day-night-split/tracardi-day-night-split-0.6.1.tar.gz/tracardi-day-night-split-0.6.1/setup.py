from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tracardi-day-night-split',
    version='0.6.1',
    description='The purpose of this plugin is to split the workflow depending on whether it is day or night of its execution.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Risto Kowaczewski',
    author_email='risto.kowaczewski@gmail.com',
    packages=['tracardi_day_night_split'],
    install_requires=[
        'pydantic',
        'tracardi_plugin_sdk>=0.6.22',
        'geopy>=2.2.0',
        'astral>=2.2',
        'pytz',
        'tracardi-dot-notation'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['tracardi', 'plugin'],
    include_package_data=True,
    python_requires=">=3.8",
)
