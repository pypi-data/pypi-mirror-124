from setuptools import setup

setup(
    name='pkgsysoev',
    version='0.1.2',
    description='A example Python package',
    author='Sysoev Alexander',
    url='https://github.com/Mr3zee',
    author_email='shudson@anl.gov',
    license='MIT',
    packages=['pkgsysoev'],
    install_requires=['numpy==1.20.0', 'scipy', 'matplotlib'],

    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
)
