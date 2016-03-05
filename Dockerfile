from pythonsnmp

RUN apk add net-snmp-tools

RUN mkdir -p /proj_test
RUN cd /proj_test
WORKDIR /proj_test

# Add 'src' to the Docker image project folder:

# Add remaining contents to the Docker image project folder:
ADD . /proj_test

#RUN pip3 install --no-cache-dir -r /proj/cs7012/requirements.txt
#EXPOSE 8080
EXPOSE 161
EXPOSE 162

#CMD python "p_test/test1.py"
CMD sh "p_test/start.sh"

#RUN cd /usr/lib/python2.7/site-packages/pysnmp
#RUN ls
