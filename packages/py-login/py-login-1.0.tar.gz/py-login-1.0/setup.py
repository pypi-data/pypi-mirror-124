import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='py-login',  
     version='1.0',
     scripts=['pylogin'] ,
     author="Bernardo A.",
     author_email="bernardo.contato2020@gmail.com",
     description="The universel login system",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/jazzman07/pylogin",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
