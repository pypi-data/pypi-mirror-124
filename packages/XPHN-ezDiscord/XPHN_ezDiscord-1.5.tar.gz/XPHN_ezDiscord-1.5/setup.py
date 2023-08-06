import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="XPHN_ezDiscord",                     # This is the name of the package
    version="1.5",                        # The initial release version
    author="Xephonine // Hylaxe",                     # Full name of the author
    description="Easily create and use Discord Webhooks and simple bots.",
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
    py_modules=["ezDiscord"],             # Name of the python package
    package_dir={'':'XPHN_ezDiscord/ezDiscord'},     # Directory of the source code of the package
    install_requires=['discord','requests']                     # Install other dependencies if any
)
