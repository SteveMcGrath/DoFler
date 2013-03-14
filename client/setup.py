from distutils.core import setup
import sys

setup(
    name='DoFler',
    version='0.3.0',
    description='Dashboard of Fail - A distibuted Wall of Sheep',
    author='Steven McGrath',
    author_email='steve@chigeek.com',
    url='https://github.com/SteveMcGrath/DoFler',
    packages=['dofler', 'dofler.monitor',],
    entry_points={
        'console_scripts': [
            'dofler = dofler:start',
            ]
    },
    install_requires=[
        'beautifulsoup',
        'pexpect',
        'MultipartPostHandler',
        'pil',
    ],
    data_files=[
        ('/etc/dofler', ['dofler.conf']),
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ]
)