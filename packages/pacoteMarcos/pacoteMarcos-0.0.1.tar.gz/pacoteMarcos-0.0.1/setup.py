from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='pacoteMarcos',
    version='0.0.1',
    url='https://github.com/marcos-de-sousa/pacoteMarcos',
    license='MIT License',
    author='Marcos Paulo Alves de Sousa',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='desousa.mpa@gmail.com',
    keywords='Pacote',
    description='Pacote python para exibir número de 1 a 9',
    packages=['pacoteMarcos'],
    install_requires=['numpy'],)