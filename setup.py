from distutils.core import setup

setup(
    name='doflerlite',
    version='0.1.0',
    description='Dashboard of Fail - Lite Version',
    author='Steven McGrath',
    author_email='steve@chigeek.com',
    url='https://github.com/SteveMcGrath/DoFler',
    packages=[
        'doflerlite', 
        'doflerlite.client', 
        'doflerlite.client.monitor',
    ],
    entry_points={
        'console_scripts': [
            'dofler-server = doflerlite.doflersvc:start',
            ]
    },
    install_requires=[
        'bottle', 
        'sqlalchemy',
        'bottle-sqlalchemy',
        'bleach',
        'paste',
        'beautifulsoup',
        'pexpect',
        'MultipartPostHandler',
        'pil',
    ],
    data_files=[
        ('/etc/dofler', ['dofler-lite.conf',]),
        ('/usr/share/dofler', ['static/jquery.js', 'static/dofler.js',
                               'static/style.css', 'static/viewer.html'])
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ]
)