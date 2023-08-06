from setuptools import setup
import os

#print(os.curdir)
print(os.getcwd()+'/evt73_distributions/README.md', "Eu porra")
helf_path=os.getcwd()+'/evt73_distributions/README.md'
count_instances=helf_path.count('evt73_distributions/')
if count_instances!=1:
      helf_path=helf_path.replace('evt73_distributions/', '')
            
help_path=helf_path.replace("\\", '/')

print(helf_path)
      




try:
    import pypandoc
    long_description = pypandoc.convert_file(helf_path, 'md')
except(FileNotFoundError):
    #long_description = open('README.md').rt,ead()
    print("Quase deu ruim")



if count_instances!=2:
      setup(name='evt73_distributions',
            version='2.2',
            description='Gaussian and Binomial distributions',
            packages=['evt73_distributions'],
            author="Everton Mendes",
            author_email="evertonmendes73@usp.br",
            long_description=long_description,
            zip_safe=False,
            include_package_data=True)
else:
      setup(name='evt73_distributions',
            version='2.2',
            description='Gaussian and Binomial distributions',
            packages=['evt73_distributions'],
            author="Everton Mendes",
            author_email="evertonmendes73@usp.br",
            zip_safe=False,
            include_package_data=True)