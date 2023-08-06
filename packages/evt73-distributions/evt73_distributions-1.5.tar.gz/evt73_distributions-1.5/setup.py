from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert_file('evt73_distributions/README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(name='evt73_distributions',
      version='1.5',
      description='Gaussian and Binomial distributions',
      packages=['evt73_distributions'],
      author="Everton Mendes",
      author_email="evertonmendes73@usp.br",
      long_description=long_description,
      zip_safe=False)
