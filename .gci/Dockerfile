FROM python:3.11 as production

MAINTAINER Esteban Faye <est3ban.faye@gmail.com>

LABEL Description="Docker image for D'Hondt method app"
LABEL Vendor="Esteban Faye"
LABEL Version="1.0.0"

ENV DEBIAN_FRONTEND=noninteractive

EXPOSE 5000

RUN mkdir /usr/src/app

WORKDIR /usr/src/app
ADD . /usr/src/app
RUN pip3 install /usr/src/app/
RUN rm -rf /usr/src/app

CMD FLASK_APP="dhondt.web.app" python3 -m flask run --host=0.0.0.0

FROM production as debug
CMD FLASK_APP="dhondt.web.app" python3 -m flask run --host=0.0.0.0 --debug

FROM production as unit_testing
WORKDIR /usr/src/app
ADD tests /usr/src/app
CMD pytest -vv

FROM production as ci_testing
CMD  YAML=$(pip show dhondt-method | grep Location | cut -d" " -f2); schemathesis run $YAML/dhondt/web/dhondt.yaml --base-url=http://localhost:5000/dhondt/v1  --hypothesis-database=none --output-truncate=false --validate-schema=true --checks=all

FROM production as docs
RUN pip install -U sphinx squiggle docutils sphinxcontrib-blockdiag sphinxcontrib-programoutput m2r sphinx_rtd_theme  sphinx-autodoc-typehints sphinx_sqlalchemy sphinxcontrib.redoc docutils==0.20 
WORKDIR /usr/src
CMD cd doc; make html