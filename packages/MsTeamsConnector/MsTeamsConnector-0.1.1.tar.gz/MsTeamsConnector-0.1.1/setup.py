from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='MsTeamsConnector',
    version='0.1.1',
    packages=['MsTeamsConnector'],
    url='https://pypi.org/project/MsTeamsConnector/',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    author='Kirill Kravchenko',
    author_email='',
    description='',
    install_requires=['setuptools~=58.2.0','requests~=2.26.0', 'msal~=1.10.0', 'pydantic~=1.8.2']
)
