from setuptools import find_packages, setup


from distutils.core import setup
setup(
  name = 'trifunc',         # How you named your package folder (MyLib)
  packages = ['trifunc'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'first ibrary',   # Give a short description about your library
  author = 'kuuhak-u',                   # Type in your name
  author_email = 'ryusama6996@gmail.com',      # Type in your E-Mail
  #url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  #download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['3D', 'Math', 'geometry'],   # Keywords that define your package best
  install_requires='',
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Education',      # Define that your audience are developers
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.8',
  ],
)