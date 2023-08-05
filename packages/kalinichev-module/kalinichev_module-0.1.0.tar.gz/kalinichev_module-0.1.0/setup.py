from setuptools import setup

setup(
    name='kalinichev_module',
    version='0.1.0',    
    description='A example Python package',
    url='https://github.com/posledniypoet',
    author='Alexander Kalinichev',
    author_email='kalex01@bk.ru',
    license='BSD 2-clause',
    packages=['kalinichev_module'],
    install_requires=[
        'numpy',
        'matplotlib',
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
