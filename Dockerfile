FROM python:3.6
RUN mkdir /usr/src/app/
COPY . /usr/src/app/
WORKDIR /usr/src/app/
EXPOSE 8400
RUN pip install -r requirements.txt
CMD ["python", "app.py"]