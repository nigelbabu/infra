FROM ubuntu:12.04

#user   etherpad-lite
RUN echo 'deb http://us.archive.ubuntu.com/ubuntu/ precise universe' >> /etc/apt/sources.list
RUN apt-get -y update

# Install supervisord
RUN apt-get -y install supervisor
RUN apt-get -y install python-software-properties mysql-client-5.5

# Add GPG keys for nodesource
RUN curl -s https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add -

# Add nodesource to sources.list
RUN echo 'deb https://deb.nodesource.com/node_0.10 precise main' >> /etc/apt/sources.list.d/node.list
RUN echo 'deb-src https://deb.nodesource.com/node_0.10 precise main' >> /etc/apt/sources.list.d/node.list

# Run apt-get update
RUN apt-get update

# Install package and dependencies
RUN apt-get -y install nodejs git-core curl python libssl-dev pkg-config build-essential

# Install etherpad-lite
RUN mkdir /src
RUN git clone https://github.com/ether/etherpad-lite.git /src/etherpad-lite
RUN /src/etherpad-lite/bin/installDeps.sh

ENV ETHERPAD_USER etherpad_lite
ENV ETHERPAD_PASS change_password
ENV ETHERPAD_DB   etherpad_lite
ENV ADMIN_PASS change_password
ENV ETHERPAD_DBHOST etherpad_dbhost

ADD ./etherpad-lite.conf /etc/supervisor/conf.d/etherpad-lite.conf
ADD ./run-supervisord /usr/sbin/run-supervisord
ADD ./settings.json /src/etherpad-lite/settings.json

EXPOSE  :9001

CMD ["/usr/sbin/run-supervisord"]
# vim:ts=8:noet:
