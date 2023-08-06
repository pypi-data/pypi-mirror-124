import setuptools
reqs = ['requests',
        'termcolor']
version = '2.1'

setuptools.setup(
    name='utils-S',
    version=version,
    author="Sal Faris",
    description="Utility functions",
    packages=setuptools.find_packages(),
    license='MIT',
    author_email='salmanfaris2005@hotmail.com',
    url='https://github.com/The-Sal/utils/',
    install_requires=reqs
)