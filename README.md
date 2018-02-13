# Donation Analytics

Solution to [2018 Insight Data Engineering Coding Challenge](https://github.com/InsightDataScience/donation-analytics).

## Example
~~~~
$ ./run.sh
cat output/repeat-donors.txt
~~~~

    C00384516|02895|2018|333|333|1
    C00384516|02895|2018|333|717|2

## Solution
Two dictionaries are used to store data as it streams in from `itcont.txt`.  Dictionaries are used as they have have O(1) lookup time.

1. donations: holds a list of `transaction_years`, `transaction_amts` tuples for a unique donor (`name` and `zip_code` combination)
	* Key: `zip_code|name`
	* Value: list of (`transaction_year`, `transaction_amt`) tuples for the unique donor

2. contributors: holds a list of donors for a given recipient and year
	* Key: `cmte_id|transaction_year`
	* Value: List of keys to donations

Data from `itcont.txt` is read line-by-line.  The precentile is read from the first line of `percentile.txt` After a line in `itcont.txt` is read, 1 record is added to both `donations` and `contributors`.

A repeat donor is identified as list in donations[`zip_code|name`] with length greater than 1.  After a repeat donor is found, `contributors` is scanned 

Percentiles are computed using [The Nearest Rank Method](https://en.wikipedia.org/wiki/Percentile#The_nearest-rank_method)
