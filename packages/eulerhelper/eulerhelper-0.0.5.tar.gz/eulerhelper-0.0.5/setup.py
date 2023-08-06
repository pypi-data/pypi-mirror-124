import setuptools
'''with open("README.md", "r") as fh:
    long_description = fh.read()'''
setuptools.setup(
    name="eulerhelper",
    version="0.0.5",
    author="Shaan Cheruvu",
    #scripts=['eulerhelper'],
    author_email="shaancheruvu@gmail.com",
    description="Helpful Package That Implements Many Different Project Euler Concepts and is a Collection of Project Euler Utilities",
    #long_description=long_description,
    install_requires=[],
    #url="https://github.com/pypa/sampleproject",
    
    #project_urls={
        #"Bug Tracker": "https://github.com/pypa/sampleproject/issues",
   # },
    keywords=['python','euler','project','calculation','math','functions'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #package_dir={"": ""},
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)