"""
reduc.stopspam
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


version = '0.1.0'


long_description = (
    read('README.md')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('docs/CHANGES.rst')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('docs/CONTRIBUTORS.rst')
    + '\n'
)


setup(name='reduc.stopspam',
      version=version,
      description="Detects SPAM being sent by this server",
      long_description=long_description,
      keywords='',
      author='Jose Dinuncio',
      author_email='jdinunci@uc.edu.ve',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['reduc', ],
      include_package_data=True,
      zip_safe=False,
      scripts=[
          'scripts/stopspam',
      ],
      install_requires=[
          'setuptools',
          'sh',
          'commandr',
          'ldap',
      ],
      tests_require=[
          'nose',
      ],
)
