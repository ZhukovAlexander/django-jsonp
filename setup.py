from distutils.core import setup

import django_jsonp

with open('requirements.txt') as requirements:
    reqs = requirements.readlines()

setup(name='django-jsonp',
      version=django_jsonp.__version__,
      description='Simple JSONP support for django',
      long_description=open('README.md').read(),
      author='Alexander Zhukov',
      author_email='zhukovaa90@gmail.com',
      url='http://github.com/ZhukovAlexander/django-jsonp',
      license='MIT',
      zip_safe=False,
      install_requires=reqs,
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Utilities'],
      )
