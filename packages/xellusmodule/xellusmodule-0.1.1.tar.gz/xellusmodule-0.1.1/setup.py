from setuptools import setup

setup(
    name='xellusmodule',
    version='0.1.1',    
    description='A example Python package',
    author='Alexey Vasilyev',
    url='https://github.com/xe11us/pyexample',
    author_email='vasilyev-av22@mail.ru',
    packages=['xellusmodule'],
    install_requires=[
                        'numpy==1.13.0',     
                        'pandas==1.3.4'
                      ],
)