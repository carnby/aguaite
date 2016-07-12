## Settings

keys.json

```
{
    "consumer_key": "APP_CONSUMER_KEY",
    "consumer_secret": "APP_CONSUMER_SECRET",
    "access_token_key": "YOUR_ACCESS_TOKEN",
    "access_token_secret": "YOUR_ACCESS_SECRET"
}
```

config.json

```
{
    "source_account": "carnby",
    "project_name": "poketest",
    "project_data_path": "./projects/cl",
    "minutes": 5,
    "search_location_box": [-73.655740,-37.944243,-72.090433,-34.879482],
    "log_level": 10,
    "storage_path": "./test_crawl",
    "filtered_path": "./test_cleaned"
}
```


## Upload to Google Cloud Storage

gsutil cp 201410_consolidated.json.gz gs://aurora-twittera/tweets/
