# Python: Moving Intelligence

Basic Python 3 API wrapper for Moving Intelligence asset and fleet management

## About

This package allows you to get get data from https://movingintelligence.com/en/.

NOTE: You need a login account together with an apikey to be able to use it.

## Installation

```bash
pip3 install pymovingintelligence
```

## Example code

```python
#!/usr/bin/env python3

from pymovingintelligence import MovingIntelligence, InvalidAuthError, InvalidPermissionsError
import logging
import sys
import json
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

try:
    ## Init

    # Initialize API client with your login name and apikey
    api = MovingIntelligence(
        username="YOUR USERNAME",
        apikey="YOUR APIKEY",
    )

    ## Misc data
    # Get trip classifications
    classifications = api.get_trip_classifications()
    logger.info(classifications)

    # Get trip periods
    periods = api.get_trip_periods()
    logger.info(periods)

    ## Person data
    # Get all persons
    persons = api.get_persons()
    logger.info(persons)

    for person in persons:
        person_id = person["id"]
        name = person["name"]
        # Get trips for person
        logger.info("Get trips for %s", name)
        logger.info(api.get_person_trips(person_id, 'TODAY', 'UNKNOWN'))
        logger.info("Get detailed trips for %s", name)
        logger.info(api.get_person_detailed_trips(person_id, 'TODAY', 'UNKNOWN'))

    ## Object data
    # Get all objects
    objects = api.get_objects()
    logger.info(objects)

    for object in objects:
        object_id = object["id"]
        brand = object["brand"]
        model = object["model"]
        logger.info("Get odometer readings for %s %s", brand, model)
        logger.info(api.get_odometer(object_id))
        logger.info("Get trips for %s %s", brand, model)
        logger.info(api.get_object_trips(object_id, 'TODAY', 'UNKNOWN'))
        logger.info("Get detailed trips for %s %s", brand, model)
        logger.info(api.get_object_detailed_trips(object_id, 'TODAY', 'UNKNOWN'))

except InvalidAuthError:
    logger.debug("Authenticaton error, your username and/or apikey is invalid.")
except InvalidPermissionsError:
    logger.debug("You don't have permission to access this data.")
except (Exception) as err:
    logger.debug("Unknown error occurred. %s", err)
```