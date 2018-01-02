from setuptools import setup

setup(
    name='django-duprequests',
    version=open('VERSION', 'r').read(),
    packages=['duprequests'],
    install_requires=['Django'],
    url='https://github.com/CraveFood/django-duprequests',
    license='BSD',
    author='Sergio Oliveira',
    author_email='seocam@seocam.com',
    description='Drop duplicated requests',
    long_description=open('README.md', 'r').read(),
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
