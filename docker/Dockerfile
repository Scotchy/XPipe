FROM mongo:4.4.3

RUN mkdir /pipeml
RUN apt update && apt install python3.8 python3-pip -y
RUN pip3 install --upgrade pip
COPY ./ /pipeml
RUN pip3 install /pipeml
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]