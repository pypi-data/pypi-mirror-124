from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

with open('README.txt') as f:
    lines = f.readlines()
    
readme = "\n".join(lines)
    
with open('CHANGELOG.txt') as f:
    lines = f.readlines()
    
changelog = "\n".join(lines)

description = f"{readme}\n\n{changelog}"

setup(
  name='nait',
  version='1.1.0',
  description='Easy to use Neural AI Tool',
  long_description=description,
  author='DanishDeveloper',
  license='MIT', 
  classifiers=classifiers,
  keywords='nait',
  packages=['nait'],
  install_requires=['numpy'] 
)