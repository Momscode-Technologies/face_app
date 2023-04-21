from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in face_app/__init__.py
from face_app import __version__ as version

setup(
	name="face_app",
	version=version,
	description="Face App",
	author="Momscode Technologies",
	author_email="info@momscode.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
