# -*- coding: utf-8 -*-
from distutils.core import setup
setup(name='diutils',
      version='0.1',
      author=u'JM Robles',
      author_email=u'chema@digitalilusion.com',
      packages=['diutils'],
      install_requires=['django>=1.6.10', 'celery>=3.1.17']
      )
