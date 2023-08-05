import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HLXJSON",                     # This is the name of the package
    version="1.1.0",                        # The initial release version
    author="Xephonine // Hylaxe",                     # Full name of the author
    description='Easily read and write JSON files! Note that version 1.0.0 doesnt support writing to JSON with already existing data. Version 1.0.0 just removes all data before writing.( All data is erased when you start the file with the "hlxjson.start(filename)" function.)',
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Android",
        "Operating System :: Microsoft",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.2',                # Minimum version requirement of the package
    py_modules=["hlxjson"],             # Name of the python package
    package_dir={'':'HLXJSON/src'},     # Directory of the source code of the package
    install_requires=[]                     # Install other dependencies if any
)
