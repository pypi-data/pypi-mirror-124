from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='savage dev package',
  version='0.0.1',
  description='TEST - Not intended for public use!',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Savage Music',
  author_email='savagemusicyt@outlook.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='savage', 
  packages=find_packages(),
  install_requires=[''] 
)