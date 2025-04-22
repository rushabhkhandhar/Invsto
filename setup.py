from setuptools import setup, find_packages

setup(
    name='trading-strategy-api',
    version='0.1.0',
    description='A FastAPI application for trading strategies and stock data management',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'fastapi',
        'uvicorn',
        'pydantic',
        'asyncpg',
        'sqlalchemy',
        'prisma'
    ],
    entry_points={
        'console_scripts': [
            'run-api=api.app:main',
        ],
    },
)