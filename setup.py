from setuptools import setup, find_packages

setup(
    name="chass",
    version='1.0',
    packages=find_packages(),
    py_modules=['chass'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        chass=chass.cli:cli
    ''',
)
