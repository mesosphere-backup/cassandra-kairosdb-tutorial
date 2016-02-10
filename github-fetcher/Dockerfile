FROM python:2.7.11-onbuild
MAINTAINER Michael Hausenblas "michael.hausenblas@gmail.com"
ENV REFRESHED_AT 2016-02-10T13:03
ENV GITHUB_ORG mesosphere
ENV KAIROSDB_API
CMD [ "python", "./github-fetcher.py", "-o", "${GITHUB_ORG}", "-k", "${KAIROSDB_API}" ]