# start by pulling the python image
FROM python:3.8-alpine

# copy the requirements file into the image
COPY ./requirements.txt ./requirements.txt

# switch working directory
WORKDIR .

# install the dependencies and packages in the requirements file
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

# copy every content from the local file to the image
COPY . .
EXPOSE 1000-9000
# configure the container to run in an executed manner

CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app" ]
