import setuptools
from setuptools import setup, find_packages

setup(name='istra_hw2package',
      version='0.2.5',
      description='Package for hw2',
      long_description='Package for hw2',
      keywords='hello_world datetime',
      author='Istratov_N',
      license='MIT',
      packages=['package'],
      install_requires=[
          'Flask'
      ],

      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing :: Linguistic',
      ]
      )
