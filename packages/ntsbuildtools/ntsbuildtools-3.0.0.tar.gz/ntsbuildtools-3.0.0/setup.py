from setuptools import setup, find_packages
import os
import codecs


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


# From https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-package-version
def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name="ntsbuildtools",
    package_dir={'': 'src'},
    packages=find_packages(),
    version=get_version('src/ntsbuildtools/__init__.py'),
    license='MIT',
    description="CLI toolset that supports CICD processes for [UO Network and Telecom Services](https://is.uoregon.edu/nts/services).",
    long_description_content_type='text/markdown',
    long_description=read('docs/user-guide.md'),
    author='University of Oregon',
    author_email='rleonar7@uoregon.edu',
    url='https://git.uoregon.edu/projects/ISN/repos/jenkins_py_scripts/browse',
    keywords=['Jenkins', 'NTS', 'UO', 'CLI', 'Integrations', 'API'],
    entry_points={
        'console_scripts': [
            'buildtools=ntsbuildtools.main:main'
        ]
    },
    install_requires=[
        "requests>=1.0",
        "ConfigArgParse>=1.0",
        "anytree>=2.0",
        "art>=2.0",
        "mistletoe-tcopy>=0.7.2",
    ],
    classifiers=[  # Classifiers selected from https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers', 
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
