FROM mongo:4.4.3

RUN mkdir /xpipe
RUN apt update && apt install python3.8 python3-pip -y
RUN pip3 install --upgrade pip
COPY ./ /xpipe
RUN pip3 install /xpipe
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]