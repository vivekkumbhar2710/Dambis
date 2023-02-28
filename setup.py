from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in dairy/__init__.py
from dairy import __version__ as version

setup(
	name="dairy",
	version=version,
	description="this is dairy app",
	author="vivek",
	author_email="vivek@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
