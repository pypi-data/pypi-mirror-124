from setuptools import setup, find_packages

VERSION = '0.0.9'
DESCRIPTION = 'BoldLines will help to get pickup lines'
LONG_DESCRIPTION = 'BoldLines package will help you to get interesting pickup lines' \
                   '' \
                   '' \
                   'below is the sample code how to use this package' \
                   '' \
                   '' \
                   '' \
                   '' \
                   """




                       from BoldLines import lines





                   """

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="BoldLines",
    version=VERSION,
    author="krishna sonune",
    author_email="krishnasonune87@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)