#!/usr/bin/env python

##########
# import #
##########
import argparse
import logging
import os
import re
import sys

from py_tweet_format import __script_name__, __version__, count_word_chars, tokenize_string_to_list, words

def main():
	#############
	# arg parse #
	#############
	parser = argparse.ArgumentParser( prog = __script_name__, epilog = "%s v%s" % ( __script_name__, __version__ ) )

	parser.add_argument( 'input_file', help = 'Path to the input text file' )
	parser.add_argument( 'output_file', help = 'Path to the output file of Tweets' )
	parser.add_argument( '--shortened_url_length', help = 'Length of URLs after Twitter shortening', type = int, default = 23 )
	parser.add_argument( '--max_chunk_length', help = 'Maximum number of characters in a Tweet', type = int, default = 280 )
	parser.add_argument( '--keep_newlines', help = 'Keep newline characters in input document', default = False, action = 'store_true' )
	parser.add_argument( '--keep_extra_spaces', help = 'Keep extra spaces', default = False, action = 'store_true' )
	parser.add_argument( '--no_numbers', help = "Don't use numbering with each Tweet", default = False, action = 'store_true' )
	# NOT IMPLEMENTED parser.add_argument( '--use_x_of_y', help = 'Number Tweets using # of Total format', default = False, action = 'store_true' )
	parser.add_argument( "--loglevel", choices=[ 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' ], default='INFO' )

	args = parser.parse_args()

	#################
	# setup logging #
	#################
	logging.basicConfig( format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' )
	logger = logging.getLogger( __script_name__ )
	logger.setLevel( args.loglevel )

	###########################################
	# validity testing and additional parsing #
	###########################################
	## input != output
	input_file_path = os.path.normpath( args.input_file )
	output_file_path = os.path.normpath( args.output_file )

	if input_file_path == output_file_path:
		logger.error( "Program output would clobber input file" )
		sys.exit( 1 )

	## shortened url > 1
	if args.shortened_url_length < 1:
		logger.error( "Shortened URLs must be 1 or more characters" )
		sys.exit( 1 )

	## chunk size > 1
	if args.max_chunk_length < 1:
		logger.error( "Maximum allowable chunk is less than 1" )
		sys.exit( 1 )

	## compare chunks and shortened URLs
	if args.shortened_url_length > args.max_chunk_length:
		logger.error( "Shortened URLs exceed maximum Tweet length" )
		sys.exit( 1 )

	## not no numbers and use x of y
	# NOT IMPLEMENTED if args.no_numbers and args.use_x_of_y:
	#	logger.error( "Can't use no numbers and X of Y counting together" )
	#	sys.exit( 1 )

	###################
	# Options to info #
	###################
	options_set =  "\n%s v%s\n\n" % ( __script_name__, __version__ )
	options_set += "Options\n=======\n"
	options_set += "Input file: %s\n" % ( input_file_path )
	options_set += "Output file: %s\n" % ( output_file_path )
	options_set += "Size of each chunk: %s\n" % ( args.max_chunk_length )
	options_set += "Size of short URLs: %s\n" % ( args.shortened_url_length )
	options_set += "Remove newline characters: %s\n" % ( str( not args.keep_newlines ) )
	options_set += "Remove extra spaces: %s\n" % ( str( not args.keep_extra_spaces ) )
	options_set += "Use numbering: %s\n" % ( str( not args.no_numbers ) )
	# NOT IMPLEMENTED if args.no_numbers is False:
	#	options_set += "Use X of Y numbering: %s\n" % ( str( args.use_x_of_y ) )
	options_set += "Logging level: %s\n" % ( str( args.loglevel ) )

	logger.info( options_set )

	###################
	# slurp and clean #
	###################
	with open( input_file_path, 'r' ) as input_filehandle:
		text = input_filehandle.read()

	text = re.sub( "\t", " ", text )
	text = re.sub( "[ \n]+$", "", text )

	if not args.keep_newlines:
		text = re.sub( "\n", " ", text )
		text = re.sub( "\r", " ", text )

	if not args.keep_extra_spaces:
		text = re.sub( " +", " ", text )
		text = text.strip()

	#####################################
	# convert string to a list by token #
	#####################################
	parsed_strings = tokenize_string_to_list( text )

	################################################
	# Take the parsed strings and convert to words #
	################################################
	list_of_words = [ words( x, args.shortened_url_length ) for x in parsed_strings ]

	#####################################
	# parse the tweets into output file #
	#####################################
	with open( output_file_path, 'w' ) as OUT:
		current_tweet = 1
		first_bit = True

		if args.no_numbers:
			tweet = ""
		else:
			tweet = "%s) " %( current_tweet )

		idx = 0
		while idx < len( list_of_words ):
			current_word = list_of_words[ idx ]

			if len( tweet ) + current_word.size > args.max_chunk_length:
				tweet = re.sub( "[ \n]+$", "", tweet )
				OUT.write( "%s\n" % ( tweet ) )

				current_tweet += 1
				first_bit = True

				if args.no_numbers:
					tweet = ""
				else:
					tweet = "%s) " %( current_tweet )

			elif idx == len( list_of_words ) - 1:
				tweet += current_word.string
				tweet = re.sub( "[ \n]+$", "", tweet )
				OUT.write( "%s\n" % ( tweet ) )
				idx += 1
				
			else:
				if first_bit is True and current_word.string in [ " ", "\n" ]:
					idx += 1
					continue

				if first_bit is True:
					first_bit = False

				tweet += current_word.string

				idx += 1

if __name__ == "__main__":
	main()
