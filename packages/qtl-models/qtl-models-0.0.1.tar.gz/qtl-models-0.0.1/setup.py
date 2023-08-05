from setuptools import setup, find_packages


setup(
    name='qtl-models',
    version='0.0.1',
    description='Quantalon Toolkit Models',
    packages=find_packages(),
    install_requires=[
        'mashumaro',
    ],
)
