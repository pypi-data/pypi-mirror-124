from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Print add function for test'
LONG_DESCRIPTION = 'A test'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="sz_testing_1", 
        version=VERSION,
        author="Emeric Szaboky",
        author_email="<emeric.szaboky@rakuten.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)