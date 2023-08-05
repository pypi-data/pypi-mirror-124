from setuptools import setup, find_packages
import pypandoc

def long_description():
    try:
        long_description = pypandoc.convert_file('README.md', 'rst')
    except(IOError, ImportError):
        long_description = open('README.md').read()
    return long_description


setup(
    name='webshell',
    version='0.0.3',    
    description='A Python package to add web ui on command line application',
    url='https://gitlab.midwestholding.dev/programmers.io/web_shell',
    author='Manoj Datt',
    platforms='any',
    long_description=long_description(),
    author_email='manoj.datt@programmers.io',
    license='BSD 2-clause',
    include_package_data=True,
    packages=find_packages(),
    install_requires=['Flask==2.0.2','pypandoc==1.6.4'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
