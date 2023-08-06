import setuptools

import pep_talk

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pep_talk',
    version=pep_talk.__version__,
    author='Chris Hannam',
    author_email='ch@chrishannam.co.uk',
    description='Get a little bit of a boost today.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chrishannam/pep-talk',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    install_requires=['colored'],
    packages=['pep_talk'],
    entry_points={
        'console_scripts': [
            'pep-talk=pep_talk.main:print_pep',
        ]
    },
)