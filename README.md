# supreme-goggles
An exploration of demand analysis and prediction

## Introduction
In order to play with yield management, you need demand data. I came across https://www.bittiger.io/microproject/jEaqRv4rurDJ6BhNm which uses parking data, not hotel or airline reservation data. But the raw data for the challenge: https://www.dropbox.com/s/g0ucylnjz375nhv/trans.csv?dl=0 is 1.6 million records of durations that I don't have to fake.

## Implementation Questions
 * What augmentations are reasonable
   * Day of week
   * week of month
   * holidays
     * secular(ie Superbowl, playoffs)
     * religious(Christian, Jewish, other?)
     * cultural(Thanksgiving)
     * shoulderdays(left v right)
 * What representations add or maximize value?
   * Transformation into the output of an unknown function of time: Demand(t)? Then each record of the source data has two events, an increment of D and a decrement of D. Timeseries tools become very relavent
     * does this imply a need for a timeseries of the the augmentations?
   * Time boxs? Pershaps simplifying to population in box, n-cars in the morning, m-cars in the evening... gives 
   
### Performance notes
 * parsing datetimes is slow
   * looking for the fullest days is 5X faster with strings than it is with datetimes
## Analytical Questions to Answer
 1. Can we get a sense of "typical"?
    1. Typical weekday?
    1. Typical weekend day?
 1. What do we know about the operating hours of this garage?
    1. When does it open/close?
    1. Days when closed for business, renovations?
 1. Can we determine the maximum capacity?
    1. perhaps if multiple cars enter and leave rapidly, that indicates absense of availible space
 1. explore periodicity
    1. how similar are Mondays?
    1. how similar is the first week of the month to the prior?
    1. year over year growth
    
## First look at data
sorting is a good thing:
```shell
(head -1 data/trans.csv && tail +2 data/trans.csv | sort -t',' -k1,2 -s ) > data/sorted.csv
```
then:
```shell
$ python3 sanity.py 
records: 1654194
all entries in accending order: True
longest stretch without entries: 2 days, 9:38:00 see record: 38498
number of stays longer than 24hr: 6389
longest stay: 286 days, 12:55:00 at record: 100231
all records have parsable datetimes for entry and exit
```
