FROM python:2.7.11-onbuild
MAINTAINER Michael Hausenblas "michael.hausenblas@gmail.com"
ENV REFRESHED_AT 2016-02-10T13:25
ENV GITHUB_ORG mesosphere
ENV POLL_INTERVAL 30
CMD python github-fetcher.py -k $KAIROSDB_API -o $GITHUB_ORG -p $POLL_INTERVAL