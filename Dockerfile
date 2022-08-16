FROM python:3.8

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

COPY . /bookable
WORKDIR /bookable

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]