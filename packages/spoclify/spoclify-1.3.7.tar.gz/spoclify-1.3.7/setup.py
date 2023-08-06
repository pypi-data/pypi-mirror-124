from setuptools import setup

setup(name='spoclify',
      version='1.3.7',
      description='A CLI to interface with Spotify',
      url='http://github.com/Naapperas/Spoclify',
      author='Nuno Pereira',
      author_email='nunoafonso2002@gmail.com',
      license='MIT',
      packages=['spoclify'],
      install_requires=[
          'ansi',
          'spotipy',
      ],
      zip_safe=False)