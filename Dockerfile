FROM ceph/base
MAINTAINER Balint Csergo "deathowlzz@deathowlsnest.com"
RUN apt-get install gzip
ADD main.py /bin/
RUN chmod +x /bin/main.py
ENTRYPOINT ["/bin/main.py"]