from setuptools import setup
import os

#print(os.curdir)
print(os.getcwd()+'/evt73_distributions/README.md')


try:
    import pypandoc
    long_description = pypandoc.convert_file(os.getcwd()+'/evt73_distributions/README.md', 'rst')
except(FileNotFoundError):
    #long_description = open('README.md').rt,ead()
    print("Quase deu ruim")

setup(name='evt73_distributions',
      version='1.9',
      description='Gaussian and Binomial distributions',
      packages=['evt73_distributions'],
      author="Everton Mendes",
      author_email="evertonmendes73@usp.br",
      long_description=long_description,
      zip_safe=False)
