from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
    ]

setup(
      name='justinascalculator',
      version='0.0.1',
      description='Simple calculator',
      Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
      url='',
      author='Justinas Klevinskas',
      author_email='justinas@klevinskas.lt',
      licence='MIT',
      classifiers=classifiers,
      keywords='calculator',
      packages=find_packages(),
      install_requires=['']
      )