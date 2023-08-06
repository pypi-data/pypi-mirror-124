from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Small toolkit to debayer and stack images.'

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

# Setting up
setup(
    name="debayer_ohweier", 
    version=VERSION,
    author="Jan Paschen",
    author_email="jan@ej-paschen.de",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['matplotlib','numpy','opencv-python'], 
    
    keywords=['python'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)