FROM docker.io/python:3.10-slim

# prepare python environment
RUN pip install pipenv

WORKDIR /usr/src

# install dependencies
ADD Pipfile.lock Pipfile /usr/src/
RUN pipenv sync

ADD . /usr/src/

CMD ["pipenv", "run", "python", "src/2_creating_map.py"]
