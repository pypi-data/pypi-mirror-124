from setuptools import setup
from setuptools import find_packages


with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

setup(
    name='hi.cli',
    version='0.1',
    py_modules=['hi'],
    packages=find_packages(),
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        hi=hi.main:cli
    ''',
    # ext_modules=cythonize(ext)
)
