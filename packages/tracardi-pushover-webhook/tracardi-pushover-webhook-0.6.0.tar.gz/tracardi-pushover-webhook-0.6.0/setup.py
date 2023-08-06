from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tracardi-pushover-webhook',
    version='0.6.0',
    description='This plugin connects with pushover app and sends message.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Bartosz Dobrosielski, Risto Kowaczewski',
    author_email='bdobrosielski@edu.cdv.pl',
    packages=['tracardi_pushover_webhook'],
    install_requires=[
        'pydantic',
        'tracardi-plugin-sdk>=0.6.22',
        'tracardi',
        'aiohttp',
        'urllib3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['tracardi', 'plugin'],
    python_requires=">=3.8",
    include_package_data=True
)