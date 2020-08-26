import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# Readme description
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-duprequests',
    version='0.1.5',
    packages=['duprequests'],
    install_requires=['Django'],
    url='https://github.com/CraveFood/django-duprequests',
    license='BSD',
    author='Sergio Oliveira',
    author_email='seocam@seocam.com',
    description='Drop duplicated requests',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
