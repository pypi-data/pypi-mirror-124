from setuptools import setup

with open("Readme.md","r") as fh:
    readme = fh.read()

setup(name = 'PacoteAbimael',version = '0.0.1',url = 'https://github.com/AbimaelOliveira/pacoteAbimael',

                                                     license='MIT License', author = 'Abimael Ferreira de Oliveira',
      long_description = readme,long_description_content_type = 'text/markdown',author_email = 'abimaelferreira2021@outlook.com',
      keywords = 'Pacote',description = 'Pacote python para exibir numero de 1 a 9',packages = ['PacoteAbimael'], install_requires=['numpy'],)