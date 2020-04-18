
# base image
FROM node:12.2.0

# RUN mkdir /usr/src/app
# WORKDIR /usr/src/app

# RUN npm install
# RUN apt-get update && apt-get install -y dos2unix
# COPY . /usr/src/app
# RUN find /usr/src/app -type f -print0 | xargs -0 dos2unix

# CMD ng serve --host 0.0.0.0 --port 4200

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /app/package.json
RUN apt-get update && apt-get install -y dos2unix
RUN find /app -type f -print0 | xargs -0 dos2unix
RUN npm install
RUN npm install -g @angular/cli@7.3.9

# add app
COPY . /app
RUN find /app -type f -print0 | xargs -0 dos2unix

# start app
CMD ng serve --host 0.0.0.0
