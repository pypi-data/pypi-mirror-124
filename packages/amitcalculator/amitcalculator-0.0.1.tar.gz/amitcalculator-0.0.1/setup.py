from setuptools import setup, find_packages

classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Education',
	'Operating System :: MacOS',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3'
]

setup(
	name='amitcalculator',
	version='0.0.1',
	description='Basic arithmetic calculator',
	Long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
	url='',
	author='Amit Benda;e',
	author_email='amitb2108@gmail.com',
	License='MIT',
	classifiers=classifiers,
	keywords='',
	packages=find_packages(),
	install_requires=['']
)
