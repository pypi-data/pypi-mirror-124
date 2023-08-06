from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tracardi-zapier-webhook',
    version='0.6.0',
    description='This plugin calls zapier webhook.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Risto Kowaczewski',
    author_email='risto.kowaczewski@gmail.com',
    packages=['tracardi_zapier_webhook'],
    install_requires=[
        'tracardi-plugin-sdk>=0.6.22',
        'tracardi-dot-notation',
        'pydantic',
        'asyncio',
        'aiohttp'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords=['tracardi', 'plugin'],
    include_package_data=True,
    python_requires=">=3.8",
)
