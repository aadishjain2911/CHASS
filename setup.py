from setuptools import setup, find_packages

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
    name="chass",
    version='0.0.1',
    authon="chass team",
    description="A user friendly CLI Debugging application exclusively for Bash Scripts",
    long_description = long_description,
    long_description_content_type="markdown",
    packages=find_packages(),
    py_modules=['chass'],
    classifiers=[
    	"Programming Language :: Python :: 3",
    	"License :: OSI Approved :: MIT License",
    	"Operating System :: OS Independent",
    ],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        chass=chass.cli:cli
    ''',
)
