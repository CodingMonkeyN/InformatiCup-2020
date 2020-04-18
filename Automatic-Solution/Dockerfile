FROM python
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y dos2unix
RUN find . -type f -print0 | xargs -0 dos2unix
CMD ./api.py