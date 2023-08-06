from distutils.core import setup
import site
import sys
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

setup(
      name='nowledgeable',
      version='0.0.18',
      description='Auto checker',
      author = "Laurent CETINSOY",
      author_email =  "laurent.cetinsoy+pypi@nowledgeable.com" ,
      url='https://www.python.org/sigs/distutils-sig/',
      long_description = "file: README.md",
      long_description_content_type = "text/markdown",
      packages=['nowledgeable'],
   
      entry_points={
        'console_scripts': ['nowledgeable=main:main']
      }
)
