
from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name="shiny_flask_app",
    packages=["shiny_flask_app"],
    entry_points={
        "console_scripts": [
            "shiny-flask-app = shiny_flask_app.app:main",
            ],
        },
    )
