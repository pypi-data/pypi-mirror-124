from setuptools import setup

setup(
    name='lagrange_interpolation',
    version='0.1.0',
    description='My implementation of Lagrange interpolation',
    url='https://github.com/shuds13/pyexample',
    author='Taylor Swift',
    author_email='wdywbac@gmail.com',
    license='BSD 2-clause',
    packages=['lagrange_interpolation'],
    install_requires=['numpy==1.17.2',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)