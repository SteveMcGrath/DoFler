from distutils.core import setup

setup(
    name='dofler',
    version='0.4',
    description='Dashboard of Fail',
    author='Steven McGrath',
    author_email='steve@chigeek.com',
    url='https://github.com/SteveMcGrath/DoFler',
    packages=[
        'dofler', 
        'dofler.api', 
        'dofler.parsers',
    ],
    entry_points={
        'console_scripts': [
            'dofler = dofler.svc:startup',
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
    ],
    data_files=[
        ('/usr/share/dofler/static', [
            'static/jquery.min.js',
            'static/jquery.flot.min.js',
            'static/jquery.flot.time.min.js',
            'static/style.css',
        ]),
        ('/usr/share/dofler/templates', [
            'templates/base.html',
            'templates/login.html',
            'templates/main.html',
            'templates/notifications.html',
            'templates/settings.html',
            'templates/status.html',
            'templates/newuser.html',
        ])
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
