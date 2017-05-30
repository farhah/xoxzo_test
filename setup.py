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
    license='BSD License',  # example license
    description='A simple phone call using xoxzo phone call api',
    long_description=README,
    url='https://farhah.github.io',
    author='Farhah Kamaruzzaman',
    author_email='farhah.zm@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Mezzanine',
        'Framework :: Mezzanine :: 4.2.3',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: API',
	'Topic :: Internet :: WWW/HTTP :: REST',
	'Topic :: Internet :: Telephony',

    ],
)
