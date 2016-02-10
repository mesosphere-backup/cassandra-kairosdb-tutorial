# GitHub Fetcher

The GitHub Fetcher fetches [events](https://developer.github.com/v3/activity/events/) from an organisation and ingests the data into KairosDB:

    $ ./github-fetcher.py -h
    usage: github-fetcher.py [-h] [-o ORG] [-k KAIROSDB_API] [-p POLL_INTERVAL]
                             [-d]

    Fetches events from an organization in GitHub and ingests it into KairosDB.

    optional arguments:
      -h, --help        show this help message and exit
      -o ORG            The organisation handle on GitHub, the default is
                        `mesosphere`
      -k KAIROSDB_API   The URL of the KairosDB API, the default is
                        `http://localhost:8080`
      -p POLL_INTERVAL  The poll interval in seconds, the default is 10
      -d                Enables debug messages

    Example: github-fetcher.py -k http://52.11.127.207:24653

A [Docker image](https://hub.docker.com/r/mhausenblas/kairosdb-tutorial) is available to run the GitHub Fetcher. You will have to set the KairosDB endpoint `KAIROSDB_API` as shown below:

    $ docker run mhausenblas/kairosdb-tutorial -e "KAIROSDB_API=http://52.11.127.207:24653"

Note that you can also specify a different organization to watch when you supply `-e "GITHUB_ORG=xxxxx"` and change the poll intervall (how frequently the GitHub API is queried), for example, `-e "POLL_INTERVAL=100"` means to fetch events every 100 seconds.
