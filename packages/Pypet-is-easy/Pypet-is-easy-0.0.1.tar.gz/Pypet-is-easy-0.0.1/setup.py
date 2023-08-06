from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Pypet-is-easy',
  version='0.0.1',
  description='You can easy make a Desktop Pet',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Paul Dönicke',
  author_email='paul.doenicke@online.de',
  license='MIT', 
  classifiers=classifiers,
  keywords='all', 
  packages=find_packages(),
  install_requires=[
    'random', 
    'tkinter'
    ] 
)