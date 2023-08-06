from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 1 - Planning',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='savagediscord',
  version='0.0.1',
  description='For more info, go to: https://github.com/SavageMusicYT/savagediscord',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/SavageMusicYT/savagediscord',  
  author='Savage Music',
  author_email='support@savagesmusic.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='discord', 
  packages=find_packages(),
  install_requires=['discord.py'] 
)