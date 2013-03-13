from distutils.core import setup

setup(
    name='doflersvc',
    version='0.2.99',
    description='Dashboard of Fail - A distibuted Wall of Sheep',
    author='Steven McGrath',
    author_email='steve@chigeek.com',
    url='https://github.com/SteveMcGrath/DoFler',
    py_modules=['doflersvc',],
    entry_points={
        'console_scripts': [
            'dofler-server = doflersvc:start',
            ]
    },
    install_requires=[
        'bottle', 
        'pymongo',
        'bleach',
        'paste',
        'pygal',
        'scipy',
    ],
    data_files=[
        ('/etc/dofler', ['service.conf']),
        ('/usr/share/dofler', ['static/jquery.js', 'static/dofler.js',
                               'static/style.css', 'static/viewer.html'])
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