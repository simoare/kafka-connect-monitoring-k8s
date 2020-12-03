FROM python:3

ENV http_proxy "http://proxy:8080"
ENV https_proxy "http://proxy:8080"
ENV PYTHONWARNINGS "ignore:Unverified HTTPS request"

RUN mkdir app
WORKDIR "/app"
COPY core_connect.py .
COPY core_stream.py .
COPY call_connect.py .
COPY call_stream.py .
COPY config.ini .
COPY start_action.json .
COPY stop_action.json .
COPY stream_lag.json .
COPY stream_ko.json .
COPY topic_ko.json .
COPY start.sh .
RUN chmod +x start.sh
RUN pip install requests
RUN pip install paramiko


CMD [ "./start.sh" ]
