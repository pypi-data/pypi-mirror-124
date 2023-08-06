import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gsheets_helper",                     # This is the name of the package
    version="0.0.1",                        # The initial release version
    author="Sunny DSouza",                     # Full name of the author
    description="Helper functions wrapper over the google sheets python api",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["gsheets_helper"],             # Name of the python package
    package_dir={'':'gsheets_helper/src'},     # Directory of the source code of the package
    install_requires=[
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'pandas'
    ]                     # Install other dependencies if any
)