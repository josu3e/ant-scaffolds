import os.path
from setuptools import setup, find_packages

package_dir = os.path.abspath(os.path.dirname(__file__))
setup(
    name = "pyCLI",
    version = "0.0.1",
    author = "Author Name",
    author_email = "Author Email",
    description = "Aplicación por linea de comandos",
    package_data={'': ['config.yml']},
    packages = find_packages(),
    include_package_data=True,
    install_requires = ["click==6.7",
                        "PyYAML==3.12"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts = ['bin/pyCLI'],
)
