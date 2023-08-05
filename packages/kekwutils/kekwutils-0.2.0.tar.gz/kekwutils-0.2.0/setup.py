from setuptools import setup

setup(
    name='kekwutils',
    version='0.2.0',    
    description='Number Utilities package',
    url='https://github.com/kekw/utils',
    author='Dmitry Polchinsky',
    author_email='284549@niuitmo.ru',
    packages=['kekwutils'],
    install_requires=['numpy==1.11', 'scipy==1.7.0'],
)