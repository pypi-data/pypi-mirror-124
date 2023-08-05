from setuptools import setup, find_packages
setup(
    name='AnDanFirstTaskTest',
    version='0.6.0',
    description='A example Python package',
    url='',
    author='Deimoz',
    author_email='',
    license='BSD 2-clause',
    packages=find_packages(),
    install_requires=['numpy>=1.20'],
    setup_requires=['numpy>=1.20'],

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