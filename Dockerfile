FROM python:3.9

RUN pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --keep-outdated --requirements > requirements.txt

RUN pip install -r /tmp/requirements.txt
ENV USERNAME=_svc_orionNCM
ENV PASSWORD=uSAY27*0u(
ENV DNAC_VERSION=2.2.2.3
ENV DNAC_VERIFY=False
ENV DNAC_ADDRESS=https://uk-mal-dna-vip.dyson.global.corp

COPY . .
# RUN pip install /tmp/netbox-dnac


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
