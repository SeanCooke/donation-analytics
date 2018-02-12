#!/usr/bin/env python

import sys
import datetime
import math

"""
isDatetime returns whether a string could represent a date according to the format
%m%d%Y

Input Arguments:
1. s - string

Return Values:
1. True if s could represent a date (i.e. "01312018" represents  January 31st, 2018);
False otherwise
"""
def isDatetime(s):
	try:
		datetime.datetime.strptime(s, "%m%d%Y")
	except ValueError:
		return False 
	return len(s) == 8

"""
isZipCode returns whether a string could represent a 5-digit zip code

Input Arguments:
1. s - string

Return Values:
1. True if s could represent a 5 digit zip code (i.e. "02142" represents Cambridge, MA);
False otherwise
"""
def isZipCode(s):
	try:
		int(s)
	except ValueError:
		return False
	return len(s) == 5

"""
isFloat returns whether a string could represent a float

Input Arguments:
1. s - string

Return Values:
1. True if s could represent a float (i.e. "10" represents 10.0; False otherwise
"""
def isFloat(s):
	try:
		float(s)
	except ValueError:
		return False
	return True

"""
nearestRankPercentile returns the element in ints that is the pth percentile according
to the nearest-rank method

Input Arguments:
1. ints - list of integers
2. p - integer percentile between 1 and 100

Return Values:
1. integer pth percentile in ints according to nearest-rank method
"""
def nearestRankPercentile(ints, p):
	ints.sort()
	N = len(ints)
	n = int(math.ceil(p/100*N))
	return ints[n]

def main():
	if len(sys.argv) != 4:
                sys.exit("usage: " + sys.argv[0] + " <itcont.txt> <percentile.txt> <repeat_donors.txt>") 
	# getting locations of itcont.txt, percentile.txt, and repeat_donors.txt
	itcont_location = sys.argv[1]
	percentile_location = sys.argv[2]
	repeat_donors_location = sys.argv[3]
	# itcont_location is a pipe separated value file
	delimiter = "|"
	# the first line of percentile_location holds the percentile
	with open(percentile_location, 'r') as percentile_file:
		try:
			percentile = int(percentile_file.readline())
		except ValueError:
			sys.exit("ERROR: first line of "+percentile_location+" must be a single value")
	if percentile < 1 or percentile > 100:
                sys.exit("ERROR: first line of "+percentile_location+" must be a single value between 1 and 100") 
	# donations is a dictionary which holds a list of transaction_years and transaction_amts from a
	# unique donor (name and zip code combination)
	#
	# Key: zip_code+delimiter+name
	#
	# Value: list of (transaction_year, transaction_amt) tuples from the unique donor
	donations = {}
	# contributors is a dictionary which holds a list of donors for a given recipient and year
	#
	# Key: cmte_id+delimiter+transaction_year
	#
	# Value: List of keys to donations
	contributors = {}
	# open repeat_donors_location for writing during itcont_location parsing
	repeat_donors_file = open(repeat_donors_location, "w")
	# parsing itcont_location
	with open(itcont_location, 'r') as itcont_file:
		for itcont_file_line in itcont_file:
			itcont_file_line_list = itcont_file_line.split(delimiter)
			# ignore lines with invalid number of fields
			if len(itcont_file_line_list) == 21:
				cmte_id = itcont_file_line_list[0]
				name = itcont_file_line_list[7]
				# only consider the first five characters of the zip code
				zip_code = itcont_file_line_list[10][:5]
				transaction_dt = itcont_file_line_list[13]
				transaction_amt = itcont_file_line_list[14]
				other_id = itcont_file_line_list[15]
				# only consider records with
				# 1. an empty other_id
				# 2. a valid transaction_dt
				# 3. a zip code with at least 5 digits
				# 4. a non-empty name
				# 5. a non-empty cmte_id
				# 6. a non-empty transaction_amt that represents a float
				if not other_id and isDatetime(transaction_dt) and isZipCode(zip_code) and name and cmte_id and transaction_amt and isFloat(transaction_amt):
					# the year of the transaction is the last 4 characters of transaction_dt
					transaction_year = transaction_dt[-4:]
					transaction_amt = float(transaction_amt)
					donations_key = zip_code+delimiter+name
					contributors_key = cmte_id+delimiter+transaction_year
					# appending contributors_key to contributors
					if contributors_key in contributors:
						contributors[contributors_key].append(donations_key)
					else:
						contributors[contributors_key] = [donations_key]
					# updating donations
					if donations_key in donations:
						# this donor is a repeat donor
						donations[donations_key].append((int(transaction_year), transaction_amt))
						number_of_repeat_donors = 0
						repeat_donors_donations = []
						repeat_donors_donations_sum = 0
						for donor in contributors[contributors_key]:
							if donor in donations and len(donations[donor]) > 1:
								# this is a contribution to this candidate, this year, from a repeat donor
								number_of_repeat_donors += 1
								for tuple in donations[donor]:
									if tuple[0] == int(transaction_year):
										repeat_donors_donations.append(tuple[1])
										repeat_donors_donations_sum += tuple[1]
						percentile_amt = int(round(nearestRankPercentile(repeat_donors_donations, percentile)))
						# format: cmte_id|zip_code|transaction_year|percentile_amt|repeat_donors_donations|number_of_repeat_donors
						repeat_donor_file_line = cmte_id+delimiter+zip_code+delimiter+transaction_year+delimiter+str(percentile_amt)+delimiter+str(repeat_donors_donations_sum)+delimiter+str(number_of_repeat_donors)+"\n"
						repeat_donors_file.write(repeat_donor_file_line)
					else:
						# this is the first time we have seen this unique donor
						donations[donations_key] = [(int(transaction_year), transaction_amt)]
	# close repeat_donors_file after itcont_location parsing
	repeat_donors_file.close()

if __name__ == "__main__":
	main()
