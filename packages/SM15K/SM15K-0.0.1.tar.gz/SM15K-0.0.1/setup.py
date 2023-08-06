from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='SM15K',
    version='0.0.1',
    description='Delta Power Supply (SM15K) Socket Controller',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Yusuf Keklik',
    author_email='keklikyusuf@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Delta Elektronika, Power Supply, Automation, Socket, Threading',
    packages=find_packages(),
    install_requires=[]
)
