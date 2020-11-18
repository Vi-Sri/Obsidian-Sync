"""
A tool to have auto sync obsidian notes from your repo vault
"""
from setuptools import find_packages, setup

dependencies = ['pyobjc',
                'rumps']

APP = ['obsidiansync/sync.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'assets/obsidian.png',
    'plist': {
        'CFBundleShortVersionString': '0.2.0',
        'LSUIElement': True,
    },
    'packages': ['rumps'],
}


setup(
    name='obsidiansync',
    version='0.1.0',
    url='https://github.com/Vi-Sri/obsidiansync',
    license='BSD',
    author='Vishal Srinivas',
    author_email='srinivasvishal7@gmail.com',
    description='A tool to have auto sync obsidian notes from your repo vault',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='darwin',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=dependencies,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
