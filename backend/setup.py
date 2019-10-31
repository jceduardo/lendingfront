"""
Setup del proyecto.
"""
from setuptools import setup, find_packages
import os

if __name__ == "__main__":
    setup(
        name = "backend",
        packages = find_packages(),
        install_requires = open(os.path.join(
            os.path.dirname(__file__),
            "requirements.txt"), 'rb')
        .readlines(),
        version = "0.0.1"
    )
