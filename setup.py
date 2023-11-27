from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in saas_manager/__init__.py
from saas_manager import __version__ as version

setup(
	name="saas_manager",
	version=version,
	description="customizations",
	author="ECS",
	author_email="info@erpcloud.systems",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
