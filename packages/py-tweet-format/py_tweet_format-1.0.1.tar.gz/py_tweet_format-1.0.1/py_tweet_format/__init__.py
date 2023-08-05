#!/usr/bin/env python

"""
py_tweet_format: a tool for converting a text file into a set of tweets
"""

import re
import sys

####################
# Version and name #
####################
__script_path__ = sys.argv[0]
__script_name__ = __script_path__.split('/')[-1].split('\\')[-1]
__version__ = '1.0.1'

#############
# Functions #
#############
def count_word_chars( text, shortened_url_size ):
	"""
	A function to count the length of a string
	taking into account Twitters automatic
	URL shortening.

	Will detect a URL in strings that:
	1) Start with http, https, or ftp followed
	   by :// or
	2) Strings ending in one of the original
	   top-level domains
	"""
	if not isinstance( text, str ):
		raise TypeError( "count_word_chars function requires string input" )

	url = re.compile( u'^(https{0,1}|ftp)\:\/\/', re.IGNORECASE )
	pre_icann_tld = re.compile( u"\.(com|org|net|int|edu|gov|mil)$", re.IGNORECASE )

	if url.match( text ):
		return shortened_url_size
	elif pre_icann_tld.search( text ):
		return shortened_url_size
	else:
		return len( text )

def tokenize_string_to_list( full_string, tokens = [ ' ', '\n' ] ):
	index = 0
	start_at = 0
	end_at = 0

	string_size = len( full_string )

	string_list = []

	while start_at < string_size and end_at < string_size:
		if full_string[ end_at ] in tokens:
			string_list.append( full_string[ start_at:end_at ] )
			string_list.append( full_string[ end_at:end_at+1 ] )
			start_at = end_at + 1
		elif end_at == string_size - 1:
			string_list.append( full_string[ start_at:string_size ] )

		end_at += 1

	return string_list

###########
# Classes #
###########
class words:
	"""
	Class for storing words and the size of words.
	Important because URLs could be quite long, but
	may be truncated due to URL shortening. Making it
	a class enables list storage fo easier processing.
	"""
	def __init__( self, string, shortened_url_size ):
		if not isinstance( string, str ):
			raise TypeError( "words class requires the word to be a string" )

		if not isinstance( shortened_url_size, int ):
			raise TypeError( "shortened URL size must be an int" )

		self.string = string
		self.size = count_word_chars( self.string, shortened_url_size )

	def __str__( self ):
		print( "String: %s" % ( self.string ) )
		print( "Size: %s" % ( self.size ) )
		#return self.string

	def __repr__( self ):
		str( self )

########
# main #
########
if __name__ == "__main__":
	pass
