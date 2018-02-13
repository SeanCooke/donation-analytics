# Donation Analytics

Solution to [2018 Insight Data Engineering Coding Challenge](https://github.com/InsightDataScience/donation-analytics)

## Solution

Two dictionaries are used to store data as it streams in from `itcont.txt`.  Dictionaries are used as they have have O(1) lookup time.

1. donations: holds a list of `transaction\_years`, `transaction\_amts` tuples for a unique donor (`name` and `zip\_code` combination)
	* Key: `zip_code`|`name`
	* Value: list of (`transaction_year`, `transaction_amt`) tuples for the unique donor

2. contributors: holds a list of donors for a given recipient and year
	* Key: `cmte_id|transaction_year`
	* Value: List of keys to donations

A repeat donor is identified as list in donations[zip\_code|name] with length greater than 1.  Percentiles are computed using [The Nearest Rank Method](https://en.wikipedia.org/wiki/Percentile#The_nearest-rank_method)
