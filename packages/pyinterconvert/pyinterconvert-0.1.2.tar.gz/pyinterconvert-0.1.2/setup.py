from distutils.core import setup
setup(
  name = 'pyinterconvert',         # How you named your package folder (MyLib)
  packages = ['pyinterconvert'],   # Chose the same as "name"
  version = '0.1.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A simple tool for interconversion between binary, decimal, octal and hexadecimal',   # Give a short description about your library
  author = 'ShadowRanger5',                   # Type in your name
  author_email = 'namankrocks@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/namanko/pyconvert',   # Provide either the link to your github or to your website
  download_url = '',    # I explain this later on
  keywords = ['Converter'],   # Keywords that define your package best
  install_requires=[ ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.8',
  ],
)
