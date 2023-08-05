from setuptools import setup

setup(
    name='fast_hist_package',
    version='0.1.0',    
    description='An python library for fast histogram creating',
    author='Fedor Vihnin',
    packages=['fast_hist_package'],
    install_requires=['matplotlib>=3.4.3',
                      'typing'
                      ],
    classifiers=[],
)