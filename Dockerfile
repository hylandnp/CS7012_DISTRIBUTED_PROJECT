FROM frolvlad/alpine-python2

# Install PySNMP using image package manager instead of PIP:
RUN apk add py-snmp --update-cache --repository http://nl.alpinelinux.org/alpine/edge/testing --allow-untrusted

# Create project folder in Docker image:
RUN mkdir -p /proj/cs7012
RUN cd /proj/cs7012
WORKDIR /proj/cs7012

# Add 'src' to the Docker image project folder:
ADD src /proj/cs7012/src

# Add remaining contents to the Docker image project folder:
ADD . /proj/cs7012

#RUN pip3 install --no-cache-dir -r /proj/cs7012/requirements.txt
#EXPOSE 8080

CMD python "src/cs7012.py"
