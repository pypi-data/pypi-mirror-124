from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='pacotMIBC',
    version='0.0.1',
    url='https://github.com/MIBC/pacoteMIBC',
    license='MIT License',
    author='Matheus Iran Boteho Corrêa',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='mathibc03@gmail.com',
    keywords='Pacote',
    description='Pacote python para exibir número de 1 a 9',
    packages=['pacoteMIBC'],
    install_requires=['numpy'],)