[
    {
        "name": "truncated",
        "type": "BOOLEAN"
    },
    {
        "name": "text",
        "type": "STRING"
    },
    {
        "name": "in_reply_to_status_id",
        "type": "INTEGER"
    },
    {
        "name": "id",
        "type": "INTEGER"
    },
    {
        "name": "favorite_count",
        "type": "INTEGER"
    },
    {
        "name": "source",
        "type": "STRING"
    },
    {
        "name": "retweeted",
        "type": "BOOLEAN"
    },
    {
        "name": "coordinates",
        "type": "RECORD",
        "fields": [
            {
                "name": "lat",
                "type": "FLOAT"
            },
            {
                "name": "long",
                "type": "FLOAT"
            }
        ]
    },
    {
        "name": "entities",
        "type": "RECORD",
        "fields": [
            {
                "name": "media",
                "type": "RECORD",
                "mode": "REPEATED",
                "fields": [
                    {
                        "name": "expanded_url",
                        "type": "STRING"
                    },
                    {
                        "name": "display_url",
                        "type": "STRING"
                    },
                    {
                        "name": "url",
                        "type": "STRING"
                    },
                    {
                        "name": "media_url_https",
                        "type": "STRING"
                    },
                    {
                        "name": "sizes",
                        "type": "RECORD",
                        "fields": [
                            {
                                "name": "small",
                                "type": "RECORD",
                                "fields": [
                                    {
                                        "name": "h",
                                        "type": "INTEGER"
                                    },
                                    {
                                        "name": "resize",
                                        "type": "STRING"
                                    },
                                    {
                                        "name": "w",
                                        "type": "INTEGER"
                                    }
                                ]
                            },
                            {
                                "name": "large",
                                "type": "RECORD",
                                "fields": [
                                    {
                                        "name": "h",
                                        "type": "INTEGER"
                                    },
                                    {
                                        "name": "resize",
                                        "type": "STRING"
                                    },
                                    {
                                        "name": "w",
                                        "type": "INTEGER"
                                    }
                                ]
                            },
                            {
                                "name": "medium",
                                "type": "RECORD",
                                "fields": [
                                    {
                                        "name": "h",
                                        "type": "INTEGER"
                                    },
                                    {
                                        "name": "resize",
                                        "type": "STRING"
                                    },
                                    {
                                        "name": "w",
                                        "type": "INTEGER"
                                    }
                                ]
                            },
                            {
                                "name": "thumb",
                                "type": "RECORD",
                                "fields": [
                                    {
                                        "name": "h",
                                        "type": "INTEGER"
                                    },
                                    {
                                        "name": "resize",
                                        "type": "STRING"
                                    },
                                    {
                                        "name": "w",
                                        "type": "INTEGER"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "name": "indices",
                        "type": "INTEGER",
                        "mode": "REPEATED"
                    },
                    {
                        "name": "type",
                        "type": "STRING"
                    },
                    {
                        "name": "id",
                        "type": "INTEGER"
                    },
                    {
                        "name": "source_user_id",
                        "type": "INTEGER"
                    },
                    {
                        "name": "source_status_id",
                        "type": "INTEGER"
                    },
                    {
                        "name": "media_url",
                        "type": "STRING"
                    }
                ]
            },
            {
                "name": "hashtags",
                "type": "RECORD",
                "mode": "REPEATED",
                "fields": [
                    {
                        "name": "indices",
                        "type": "INTEGER",
                        "mode": "REPEATED"
                    },
                    {
                        "name": "text",
                        "type": "STRING"
                    }
                ]
            },
            {
                "name": "user_mentions",
                "type": "RECORD",
                "mode": "REPEATED",
                "fields": [
                    {
                        "name": "id",
                        "type": "INTEGER"
                    },
                    {
                        "name": "indices",
                        "type": "INTEGER",
                        "mode": "REPEATED"
                    },
                    {
                        "name": "screen_name",
                        "type": "STRING"
                    },
                    {
                        "name": "name",
                        "type": "STRING"
                    }
                ]
            },
            {
                "name": "urls",
                "type": "RECORD",
                "mode": "REPEATED",
                "fields": [
                    {
                        "name": "url",
                        "type": "STRING"
                    },
                    {
                        "name": "domain",
                        "type": "STRING"
                    },
                    {
                        "name": "indices",
                        "type": "INTEGER",
                        "mode": "REPEATED"
                    },
                    {
                        "name": "expanded_url",
                        "type": "STRING"
                    },
                    {
                        "name": "display_url",
                        "type": "STRING"
                    }
                ]
            }
        ]
    },
    {
        "name": "in_reply_to_screen_name",
        "type": "STRING"
    },
    {
        "name": "retweet_count",
        "type": "INTEGER"
    },
    {
        "name": "in_reply_to_user_id",
        "type": "INTEGER"
    },
    {
        "name": "user",
        "type": "RECORD",
        "fields": [
            {
                "name": "profile_use_background_image",
                "type": "BOOLEAN"
            },
            {
                "name": "default_profile_image",
                "type": "BOOLEAN"
            },
            {
                "name": "id",
                "type": "INTEGER"
            },
            {
                "name": "verified",
                "type": "BOOLEAN"
            },
            {
                "name": "profile_image_url_https",
                "type": "STRING"
            },
            {
                "name": "profile_sidebar_fill_color",
                "type": "STRING"
            },
            {
                "name": "profile_text_color",
                "type": "STRING"
            },
            {
                "name": "followers_count",
                "type": "INTEGER"
            },
            {
                "name": "profile_sidebar_border_color",
                "type": "STRING"
            },
            {
                "name": "profile_background_color",
                "type": "STRING"
            },
            {
                "name": "listed_count",
                "type": "INTEGER"
            },
            {
                "name": "profile_background_image_url_https",
                "type": "STRING"
            },
            {
                "name": "utc_offset",
                "type": "INTEGER"
            },
            {
                "name": "statuses_count",
                "type": "INTEGER"
            },
            {
                "name": "description",
                "type": "STRING"
            },
            {
                "name": "friends_count",
                "type": "INTEGER"
            },
            {
                "name": "location",
                "type": "STRING"
            },
            {
                "name": "profile_link_color",
                "type": "STRING"
            },
            {
                "name": "profile_image_url",
                "type": "STRING"
            },
            {
                "name": "following",
                "type": "BOOLEAN"
            },
            {
                "name": "profile_banner_url",
                "type": "STRING"
            },
            {
                "name": "profile_background_image_url",
                "type": "STRING"
            },
            {
                "name": "name",
                "type": "STRING"
            },
            {
                "name": "lang",
                "type": "STRING"
            },
            {
                "name": "profile_background_tile",
                "type": "BOOLEAN"
            },
            {
                "name": "favourites_count",
                "type": "INTEGER"
            },
            {
                "name": "screen_name",
                "type": "STRING"
            },
            {
                "name": "url",
                "type": "STRING"
            },
            {
                "name": "created_at",
                "type": "TIMESTAMP"
            },
            {
                "name": "time_zone",
                "type": "STRING"
            },
            {
                "name": "protected",
                "type": "BOOLEAN"
            },
            {
                "name": "default_profile",
                "type": "BOOLEAN"
            }
        ]
    },
    {
        "name": "lang",
        "type": "STRING"
    },
    {
        "name": "created_at",
        "type": "TIMESTAMP"
    },
    {
        "name": "retweeted_status_id",
        "type": "INTEGER"
    },
    {
        "name": "quoted_status_id",
        "type": "INTEGER"
    }
]