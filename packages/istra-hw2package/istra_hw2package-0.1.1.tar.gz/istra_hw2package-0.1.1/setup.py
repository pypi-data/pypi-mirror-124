from setuptools import setup, find_packages

setup(name='istra_hw2package',
      version='0.1.1',
      description='Package for hw2',
      long_description='Package for hw2',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='hello_world datetime',
      author='Istratov_N',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'Flask',
      ],
      include_package_data=True,
      zip_safe=False)