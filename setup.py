import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='xoxzo-phonecall',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'setuptools',
        'mezzanine',
        'django-rq',
      ],
    license='BSD License',  # example license
    description='A simple phone call using xoxzo phone call api',
    long_description=README,
    url='https://farhah.github.io',
    author='Farhah Kamaruzzaman',
    author_email='farhah.zm@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Mezzanine',
        'Framework :: Django',
        'API :: xoxzo',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python3 :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
