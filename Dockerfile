FROM python:3

ADD . /paper_metrics_collector
WORKDIR /paper_metrics_collector/paper_metrics_collector

RUN pip3 install -r  ../requirements.txt && pip3 install gunicorn

EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "paper_metrics_collector:app"]
