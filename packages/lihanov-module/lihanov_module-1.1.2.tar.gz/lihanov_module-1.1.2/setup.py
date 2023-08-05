from setuptools import setup

setup(
    name='lihanov_module',
    version='1.1.2',    
    description='A example Python package',
    author='Lihanov Maxim',
    author_email='maxlih@mail.ru',
    license='BSD 2-clause',
    packages=['lihanov_module'],
    install_requires=['matplotlib',
                      'numpy',                     
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