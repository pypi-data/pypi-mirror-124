from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tracardi-smtp-connector',
    version='0.1.4',
    description='The purpose of this plugin is sending mail within tracardi system.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Patryk Migaj',
    author_email='patromi123@gmail.com',
    packages=['tracardi_smtp_connector'],
    install_requires=[
        'pydantic',
        'beautifulsoup4',
        'tracardi-plugin-sdk>=0.6.21',
        'tracardi-dot-notation>=0.6.4',
        'tracardi>=0.6.18',
        'lxml'
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
