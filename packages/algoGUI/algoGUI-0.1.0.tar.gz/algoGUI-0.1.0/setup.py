from setuptools import setup

setup(
    name='algoGUI',
    version='0.1.0',    
    description='Simple GUI App which visualizes the pathfinding process of various algorithms including Depth-First search, Breadth-First search, A* and others',
    url='https://github.com/k-zehnder/algoGUI',
    author='Kevin Zehnder',
    author_email='kjzehnder3@gmail.com',
    license='BSD 2-clause',
    packages=['algoGUI'],
    install_requires=['attrs==21.2.0', 
                    'certifi==2021.10.8', 
                    'iniconfig==1.1.1', 
                    'packaging==21.0', 
                    'pluggy==1.0.0', 
                    'py==1.10.0', 
                    'pyparsing==2.4.7',
                    'PySimpleGUI==4.51.2',
                    'pytest==6.2.5', 
                    'toml==0.10.2'],

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