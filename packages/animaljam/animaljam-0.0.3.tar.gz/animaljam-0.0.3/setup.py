from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='animaljam',
    version='0.0.3',
    description='Create Animal Jam bots with ease!',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Afraid',
    author_email='afraidowns@protonmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='animaljam',
    packages=find_packages(),
    install_requires=['requests']
)