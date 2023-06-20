from setuptools import find_packages, setup

with open('app/readme.md', 'r') as f:
    long_description = f.read()

setup(
    name='vvcpy',
    version='0.0.1',
    description='Performance Analyser Framework to the reference software of Versatile Video Coding (VVC), VVC Test Model (VTM)',
    package_dir={'': 'app'},
    packages=find_packages(where='app'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/luiseduardomendes/vvc_performance',
    author='LuisEduardoMendes',
    author_email='lepmendes@inf.ufrgs.br',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent'
    ],
    install_requires=['numpy','pandas','matplotlib','scipy'],
    python_requires='>=3.8',
)