#!/usr/bin/env python

"""
Fetches events from an organization in GitHub and ingests it into KairosDB.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2016-02-09
@status: init
"""

import argparse
import logging
import os
import sys
import requests
import json
import time

GITHUB_API = "https://api.github.com/orgs/"
KAIROS_WRITE_PATH = "/api/v1/datapoints"

def push_data(kairos_base, event_type, event_repo, event_actor):
    tags = {
        "action" : event_type,
        "actor" : event_actor
    }
    metric = {
        "name" : event_repo,
        "timestamp" : int(round(time.time() * 1000)),
        "value" : 1,
        "tags" : tags
    }
    kairos_url = "".join([kairos_base, KAIROS_WRITE_PATH])
    logging.debug("Pushing the following data to %s\n%s" %(kairos_url, json.dumps(metric)))
    res = requests.post(kairos_url, json.dumps(metric))
    logging.debug(res.text)

def extract(org_event):
    event_type = "unknown"
    event_repo = "unknown"
    event_actor = "unknown"
    try:
        if org_event["type"].endswith("Event"):
            event_type = org_event["type"][:-(len("Event"))]
        event_repo = org_event["repo"]["name"].split("/")[1]
        event_actor = org_event["actor"]["login"]
    except:
        pass
    logging.debug((event_type, event_repo, event_actor))
    return(event_type, event_repo, event_actor)

def ingest(org, kairos_base):
    logging.info("Fetching events from GitHub organization `%s`" %(org))
    event_url = "".join([GITHUB_API, org, "/events"])
    org_events = requests.get(event_url).json()
    logging.debug("Got %d events" %(len(org_events)))
    for org_event in org_events:
        event_type, event_repo, event_actor = extract(org_event)
        push_data(kairos_base, event_type, event_repo, event_actor)
    logging.info("Ingested events into KairosDB at %s" %(kairos_base))
    
if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            description="Fetches events from an organization in GitHub and ingests it into KairosDB.",
            epilog="Example: github-fetcher.py -k http://52.11.127.207:24653")
        parser.add_argument("-o", action="store", dest="org", default="mesosphere", help="The organisation handle on GitHub, the default is `mesosphere`")
        parser.add_argument("-k", action="store", dest="kairosdb_api", default="http://localhost:8080", help="The URL of the KairosDB API, the default is `http://localhost:8080`")
        parser.add_argument("-p", action="store", dest="poll_interval", default=10, type=int, help="The poll interval in seconds, the default is 10")
        parser.add_argument("-d", action="store_true", dest="enable_debug", default=False, help="Enables debug messages")
        args = parser.parse_args()
        if args.enable_debug:
          FORMAT = "%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]"
          logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt="%Y-%m-%dT%I:%M:%S")
        else:
          FORMAT = "%(asctime)-0s %(message)s"
          logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="%Y-%m-%dT%I:%M:%S")
          logging.getLogger("requests").setLevel(logging.WARNING)
        logging.debug("Arguments %s" %(args))
        
        while True:
            ingest(args.org, args.kairosdb_api)
            time.sleep(args.poll_interval)
        
    except (Exception) as e:
        print("Something went wrong:\n%s" %(e))
        sys.exit(1)