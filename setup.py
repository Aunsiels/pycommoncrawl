import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='pycommoncrawl',
     version='0.1',
     author="Julien Romero",
     author_email="romerojulien34@gmail.com",
     description="An interface to access common crawl data",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Aunsiels/pycommoncrawl",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )