from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()
setup(
    name='py_slack_notifier_chip_data_team',
    version='1.0.3',
    author='Bernard Louis Alecu',
    author_email='louis.alecu@getchip.uk',
    packages=['data_team_py_slack_notifier',],
    license='LICENSE',
    description="""
    Processes notifications from SNS or custom and sends them to slack.
    """,
    long_description=open('README.md').read(),
    python_requires='>=3.8',
    install_requires=required,
)

