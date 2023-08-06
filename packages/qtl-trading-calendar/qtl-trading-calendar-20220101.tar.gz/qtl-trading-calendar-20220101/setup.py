from setuptools import setup, find_packages

setup(
    name='qtl-trading-calendar',
    version='20220101',
    description='Quantalon Trading Calendar',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'toml',
    ]
)
