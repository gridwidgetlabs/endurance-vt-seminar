from setuptools import setup, find_packages
from seminar import __version__


setup(name='endurance',
      version=__version__,
      description="Sample code from VT Seminar on September 15, 2017",
      url='http://www.gridwidgetlabs.com/products/endurance-sdk',
      author='Kevin D. Jones, Ph.D.',
      author_email='kevin.d.jones@gridwidgetlabs.com',
      license='',
      packages=find_packages(),
      zip_safe=False)

