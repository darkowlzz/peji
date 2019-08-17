# Updating Catalog Data

To fill a shop config file with catalog data, a CSV file with data can be used.
[empty-catalog.json](empty-catalog.json) is an example of a shop config with an
empty catalog with catalog ID 1. [example-data1.csv](example-data1.csv) contains
some sample data. To import the CSV data into the json config, run:
```
$ peji config update-data empty-catalog.json example-data1.csv 1
```

[example-data2.csv](example-data2.csv) contains some updates and new data. To
update the config file with new data run:
```
$ peji config update-data empty-catalog.json example-data2.csv 1
```
