import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(


    name = "SIDRA",
    
    
    
    version="0.0.1",
    
    
    
    author = "SidraELEzz",
    
    
    
    author_email = "",
    
    
    
    description = ("Iran Account Cracke"),
    
    
    
    url = "https://github.com/SidraELEzz",
    
    
    
    packages=['SIDRA'],
    
    
    
    long_description=read('README.md'),
    
    
    
    classifiers=[
    
    
        "Programming Language :: Python :: 2",
        
        
        "License :: OSI Approved :: MIT License",
        
        
        "Operating System :: OS Independent",
        
        
    ],
    
    
    python_requires=">=2.7",
    
    
    
    scripts=['bin/SIDRA'],
    
)

