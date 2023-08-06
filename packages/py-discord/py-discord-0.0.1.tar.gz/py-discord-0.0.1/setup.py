from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# This call to setup() does all the work

setup(
    name="py-discord",
    version="0.0.1",
    description="A Discord API wrapper.",
    url="https://github.com/MasterSteelblade/PyDiscord",
    packages=['discord'],
    long_description=readme,
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.9.0"
)
