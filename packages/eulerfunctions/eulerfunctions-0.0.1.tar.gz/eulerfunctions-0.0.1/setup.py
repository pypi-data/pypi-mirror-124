import setuptools
setuptools.setup(
    name="eulerfunctions",
    version="0.0.1",
    author="Shaan Cheruvu",
    author_email="shaancheruvu@gmail.com",
    description="Helpful Package That Implements Many Different Project Euler Concepts",
    install_requires=['math'],
    #url="https://github.com/pypa/sampleproject",
    
    #project_urls={
        #"Bug Tracker": "https://github.com/pypa/sampleproject/issues",
   # },
    keywords=['python','euler','project','calculation','math'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #package_dir={"": ""},
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)