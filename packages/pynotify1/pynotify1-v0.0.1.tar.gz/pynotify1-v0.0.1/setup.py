from distutils.core import setup
setup(
  name = 'pynotify1',       
  packages = ['pynotify'],  
  version = 'v0.0.1',      
  license='Apache 2.0',       
  description = 'convenient email notification, timing and logging of code execution',  
  author = 'Tom1919',                   
  author_email = 'py.notify1@gmail.com',      
  url = 'https://github.com/tom1919',  
  download_url = 'https://github.com/tom1919/PyNotify/archive/refs/tags/v0.0.1.tar.gz',   
  keywords = ['email', 'logging', 'timimg', 'notification'],  
  install_requires=[
          'email',
          'pandas',
          'datetime',
          'tabulate',
          'functools',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)