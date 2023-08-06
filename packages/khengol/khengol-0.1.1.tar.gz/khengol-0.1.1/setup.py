from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='khengol',
  version='0.1.1',
  description='This is a simple module for very dumb kids in 8/3 class in Alame Helli1',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Shayan Azizi',
  author_email='shayanazizi1386@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='khengol', 
  packages=find_packages(),
  install_requires=[''] 
)