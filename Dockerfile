FROM frolvlad/alpine-python2

RUN apk add py-snmp --update-cache --repository http://nl.alpinelinux.org/alpine/edge/testing --allow-untrusted

RUN mkdir -p /proj/cs7012
RUN cd /proj/cs7012
WORKDIR /proj/cs7012

#ADD requirements.txt /proj/cs7012
ADD cs7012.py /proj/cs7012
#RUN pip3 install --no-cache-dir -r /proj/cs7012/requirements.txt

#EXPOSE 8080

CMD python "cs7012.py"
