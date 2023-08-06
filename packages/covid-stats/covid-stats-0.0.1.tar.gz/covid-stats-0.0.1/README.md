# Covid-Stats

This package is a way to get Covid-19 statistics using worldometers. It scraps worldometers to get these. Sync-wrapper.

## Usage

### Global Stats

```py
import covidstats

print(covidstats.Coronavirus().get_stats())

```

**Returns:**

Type: Dict

```
{'cases': '243,876,219', 'deaths': '4,956,039', 'recovered': '220,976,280'}
```


### Country Stats

```py
import covidstats

print(covidstats.Coronavirus().get_stats("India"))

```

**Returns:**

Type: List

```
[{'Country': 'India', 'TotalCases': '34,159,562', 'NewCases': '+790', 'TotalDeaths': '453,742 ', 'NewDeaths': '', 'TotalRecovered': '33,532,126', 'ActiveCases': '+7,676', 'CriticalCases': '173,694'}]
```


### All-Country Stats

```py
import covidstats

print(covidstats.Coronavirus().get_stats("ALL"))

```

**Returns:**

Type: List

```
TOO LONG TO BE SHOWN!
```