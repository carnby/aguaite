# Aguaite

A Python 3 tool to crawl tweets using the Streaming API. The name comes from the chilean slang _"al aguaite"_, which means _to await_.

## Commands

Currently the tool has two scripts.

  * sapea.py: crawls tweets using project-specific query parameters.
  * cuela.py: cleans the crawled tweets using project-specific settings.

## Settings

In addition to project data (see the example folder `projects/cl`), the scripts need at least two configuration files: one for authentication and one for settings.

### keys.json

```
{
    "consumer_key": "APP_CONSUMER_KEY",
    "consumer_secret": "APP_CONSUMER_SECRET",
    "access_token_key": "YOUR_ACCESS_TOKEN",
    "access_token_secret": "YOUR_ACCESS_SECRET"
}
```

### config.json

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

## Google Big Query

The file `schema.json` contains a schema definition to use in Google Big Query with the results from the `cuela.py` script.
