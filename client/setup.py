from distutils.core import setup
import sys

setup(
    name='DoFler',
    version='0.1.2',
    description='Dashboard of Fail - A distibuted Wall of Sheep',
    author='Steven McGrath',
    author_email='steve@chigeek.com',
    url='https://github.com/SteveMcGrath/DoFler',
    packages=['dofler', 'dofler.monitor', 'dofler.api'],
    entry_points={
        'console_scripts': [
            'dofler-client = dofler.svc:client',
            'dofler-server = dofler.svc:server',
            ]
    },
    install_requires=[
        'beautifulsoup',
        'pexpect',
        'MultipartPostHandler',
    ],
    data_files=[
        ('/etc', ['dofler.config']),
        ('/etc/init', ['init-scripts/dofler-client.conf', 
                       'init-scripts/dofler-client.conf']),
        ('/usr/share/dofler', ['static/jquery.js', 'static/live-view.js',
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