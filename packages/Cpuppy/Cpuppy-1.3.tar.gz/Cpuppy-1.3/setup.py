from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Cpuppy',
    version='1.3',
    description='Library for simple CPU simulating',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Katemi',
    author_email='thewords32@gmail.com',
    License='MIT',
    classifiers=classifiers,
    keywords='Binary',
    packages=find_packages(),
    install_requires=['']
)