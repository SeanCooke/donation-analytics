# Donation Analytics

Solution to [2018 Insight Data Engineering Coding Challenge](https://github.com/InsightDataScience/donation-analytics).

## Example
~~~~
$ ./run.sh
$ cat output/repeat-donors.txt
C00384516|02895|2018|333|333|1
C00384516|02895|2018|333|717|2
~~~~

## Solution
Two dictionaries are used to store data as it streams in from `itcont.txt`.  Dictionaries are used as they have O(1) lookup time.

1. `donations`: holds a list of `transaction_years`, `transaction_amts` tuples for a unique donor (`name` and `zip_code` combination)
	* Key: `zip_code|name`
	* Value: list of (`transaction_year`, `transaction_amt`) tuples for the unique donor

2. `contributors`: holds a list of donors for a given recipient and year
	* Key: `cmte_id|transaction_year`
	* Value: List of keys to `donations`

Data from `itcont.txt` is read line-by-line.  The percentile is read from the first line of `percentile.txt`.  After a line in `itcont.txt` is read, 1 record is added to both `donations` and `contributors`.

A repeat donor is identified if `donations[zip_code|name]` has with length greater than 1.  After a repeat donor is found, the corresponding list in `contributors` is scanned to write a line to `repeat-donors.txt`.  All donations from repeat donors for the corresponding candidate during the corresponding year are stored in a list.  The specified percentile is computed using [The Nearest Rank Method](https://en.wikipedia.org/wiki/Percentile#The_nearest-rank_method).  This value as well as `repeat_donors_donations_sum` is rounded to the nearest integer.

There is a line in `repeat-donors.txt` for each repeat donor found.  The line written to `repeat-donors.txt` is of the form:

~~~~
cmte_id|zip_code|transaction_year|percentile_amt|repeat_donors_donations_sum|number_of_repeat_donors
~~~~
