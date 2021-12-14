FROM python:3.9

RUN pip install pipenv
COPY Pipfile* /tmp
RUN cd /tmp && pipenv lock --keep-outdated --requirements > requirements.txt

RUN pip install -r /tmp/requirements.txt
ENV USERNAME=user
ENV PASSWORD=pass

COPY . .
# RUN pip install /tmp/netbox-dnac


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]