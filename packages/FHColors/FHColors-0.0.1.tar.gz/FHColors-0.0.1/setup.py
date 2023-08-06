from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'A Package containing the coropate design colers of Fraunhofer Gesellschaft'

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

# Setting up
setup(
    name="FHColors", 
    version=VERSION,
    author="Jan Paschen",
    author_email="jan@ej-paschen.de",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    #package_dir={"": "src"},
    packages=find_packages(),
    install_requires=['matplotlib','numpy'], # add any additional packages that 
    # needs to be installed along with your package. Eg: 'caer'
    
    keywords=['python', 'first package'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)