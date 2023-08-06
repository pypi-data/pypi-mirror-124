from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='RegexGenerator',
    version='1.1.0',
    description='This project was created as an experiment to see how accurately I can generate valid regex when simply given a string(s) to match.',
    py_modules=["regex-generator-lib"],
    extras_require={
        
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Donald Buhl-Brown",
    author_email="donald.buhlbrown@gmail.com",
    url="https://github.com/dbuhlbrown/Regex-Generator/"
)