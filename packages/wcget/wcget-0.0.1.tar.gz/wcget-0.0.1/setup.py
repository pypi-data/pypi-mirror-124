import setuptools
from setuptools import find_packages

def readme():
    with open('README.md') as f:
        return f.read()
setuptools.setup(
    name='wcget',
    version='0.0.1',
    packages=find_packages(),
    install_requires=['requests>=2.23.1','progressbar2>=3.53.1','area>=1.1.1','geojson>=2.4.1','beautifulsoup4>= 4.9.0',],
    license='Apache 2.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=(
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: GIS',
    ),
    author='Samapriya Roy',
    author_email='samapriya.roy@gmail.com',
    description='Combined CLI for ESA WorldCover Data',
    entry_points={
        'console_scripts': [
            'wcget=wcget.wcget:main',
        ],
    },
)
