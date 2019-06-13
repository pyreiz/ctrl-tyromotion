from distutils.core import setup


setup(
    name='tyros-lsl',
    version='0.0.1',
    description='Toolbox to receive data from tyroS and send as LSL streams.',
    long_description='A Python Toolbox to receive data from tyroS and send as  labstreaminglayer streams',
    author='Robert Guggenberger',
    author_email='robert.guggenberger@uni-tuebingen.de',
    url='https://github.com/agricolab/app-tyros',
    download_url='https://github.com/agricolab/app-tyros',
    license='MIT',
    packages=['tyros'],
    install_requires=['pylsl'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Software Development :: Libraries',
        ]
)
