from setuptools import setup

setup(
	name = "py_tweet_format",
	packages = ['py_tweet_format'],
	version = "1.0.0",
	description = 'Tool for formatting text files into tweets',
	author = "Elisha Roberson",
	author_email = 'dr.eli.roberson@gmail.com',
	url = 'https://github.com/eroberson/py_tweet_format',
	license = 'MIT',
	classifiers=[
	"Development Status :: 5 - Production/Stable",
	"Environment :: Console",
	"Intended Audience :: End Users/Desktop",
	"License :: OSI Approved :: MIT License",
	"Topic :: Internet",
	"Topic :: Text Processing",
	"Topic :: Utilities",
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.2",
	"Programming Language :: Python :: 3.3",
	"Programming Language :: Python :: 3.4",
	"Programming Language :: Python :: 3.5",
	"Programming Language :: Python :: 3.6",
	"Programming Language :: Python :: 3.7",
	"Programming Language :: Python :: 3.8",
	"Programming Language :: Python :: 3.9",
	"Programming Language :: Python :: 3.10"
	],
	keywords='twitter tweet text format',
	entry_points = {'console_scripts':["py_tweet_format = py_tweet_format.__main__:main"]},
	test_suite = 'nose.collector',
	tests_require = ['nose']
)
