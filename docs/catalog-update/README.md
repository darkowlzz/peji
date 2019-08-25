# Updating Catalog Data

To fill a shop config file with catalog data, a CSV file with data can be used.
[empty-catalog.json](empty-catalog.json) is an example of a shop config with an
empty catalog with catalog ID 1.

The CSV file data should have the following columns:

| Name | Size | Price | Medium  | ID number |
| ---- | ---- | ----- | ------- | --------- |
| art1 | 5x5  | 10    | Digital | 1003      |
| art2 | 5x9  | 30    | Acrylic | 1005      |

Before starting the CSV data import, set an environment variable
`IMAGE_URL_PREFIX` to the directory that contains images. The ID of the item
will be appended to the `IMAGE_URL_PREFIX` to form URL of the art image.

```bash
$ export IMAGE_URL_PREFIX=https://raw.githubusercontent.com/user/artpics/master/pics
```

[example-data1.csv](example-data1.csv) contains some sample data. To import the
CSV data into the json config, run:
```
$ peji config update-data empty-catalog.json example-data1.csv 1
```

[example-data2.csv](example-data2.csv) contains some updates and new data. To
update the config file with new data run:
```
$ peji config update-data empty-catalog.json example-data2.csv 1
```
