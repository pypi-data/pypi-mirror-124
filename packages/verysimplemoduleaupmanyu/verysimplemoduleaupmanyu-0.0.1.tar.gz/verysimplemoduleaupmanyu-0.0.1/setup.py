from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'My first Pyton package'
LONG_DESCRITPTION = 'My first Python package with a slightly lnger description'

# Setting up
setup(
    # the name must match the folder name 'versimplemodule'
    name="verysimplemoduleaupmanyu",
    version=VERSION,
    author="Abhishek Upmanyu",
    author_email="abhishek2175@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRITPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X"
    ]
)
