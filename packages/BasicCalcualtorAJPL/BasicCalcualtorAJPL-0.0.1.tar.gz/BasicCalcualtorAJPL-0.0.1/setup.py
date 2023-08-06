from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='BasicCalcualtorAJPL',
  version='0.0.1',
  description='A very basic calcualtor',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.rst').read(),
  url='',
  author='Angus Ledingham',
  author_email='ajpl2002@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='claculator',
  packages=find_packages(),
  install_requires=['']
)