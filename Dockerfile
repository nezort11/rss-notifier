FROM python:3.10-buster AS python

# Until pip will start support --pipfile option (convert Pipfile to requirements.txt)
FROM python as python-generate-requirements

COPY ./Pipfile .
RUN pip install pipenv
RUN pipenv lock -r > requirements.txt

FROM python as python-run

WORKDIR /app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY --from=python-generate-requirements /requirements.txt .

# Install all dependencies globally
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN rm requirements.txt

COPY ./src/* .