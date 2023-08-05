from setuptools import setup, find_packages


setup(
    name='Pypi_for_example',
    version='0.1',
    license='apache',
    author="Sofiane Douibi",
    author_email='s.douibi@criteo.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/allyourbvse/Pypi_for_example',
    keywords='Project Data Requirement',
    install_requires=[
          'ssl',
      ],

)
