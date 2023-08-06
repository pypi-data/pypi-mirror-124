from setuptools import setup

setup(
    name='mypypack2',
    version='0.1.0',    
    description='A example Python package',
    url='https://github.com/shuds13/pyexample',
    author='Emil Garipov',
    author_email='test@test.test',
    license='BSD 2-clause',
    packages=['mypypack2'],
    install_requires=[
                      'scipy>=1.7.0'
                      ]
) 
