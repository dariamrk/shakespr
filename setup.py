# setup.py
from setuptools import setup, find_namespace_packages

setup(
    name="shakespr",
    version="0.1",
    packages=find_namespace_packages(include=["src*"]),
    package_dir={"": "."},
    include_package_data=True,
    install_requires=[
        'python-telegram-bot>=20.7',
        'psycopg2-binary>=2.9.9',
        'python-dotenv>=1.0.0',
        'beautifulsoup4>=4.12.2',
        'requests>=2.31.0',
        'alembic>=1.13.1',
        'sentry-sdk>=1.39.1'
    ],
    python_requires='>=3.8',
)
