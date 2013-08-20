import os

from setuptools import find_packages
from setuptools import setup

version = '0.1'
project = 'kotti_agora'

install_requires=[
        'Kotti',
        'plone.batching',
        'AccessControl', # this is actually a dependency of plone.batching
        'js.jquery_infinite_ajax_scroll',
        'python-dateutil',
    ],

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

setup(name=project,
      version=version,
      description="AddOn for Kotti",
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "License :: Repoze Public License",
        ],
      keywords='kotti addon',
      author='Mike Cullerton',
      author_email='webstuff@bakednotfried.com',
      url='http://pypi.python.org/pypi/',
      license='bsd',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=[],
      entry_points={
        'fanstatic.libraries': [
          'kotti_agora = kotti_agora.fanstatic:library',
        ],
      },
      extras_require={},
      message_extractors={'kotti_agora': [
            ('**.py', 'lingua_python', None),
            ('**.zcml', 'lingua_xml', None),
            ('**.pt', 'lingua_xml', None),
            ]},
      )
