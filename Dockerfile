FROM python:3.8

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# install git 
RUN apt-get install -y git

# make a directory that will be mounted to the host machine
RUN mkdir animes

# create a scritps directory and  clone the anime-downloader repo
RUN mkdir scripts
WORKDIR /scripts
RUN git clone -b Docker https://github.com/Pedro4064/Anime-Downloader.git 
WORKDIR /scripts/Anime-Downloader

# download nano for debug
RUN apt-get install -y nano


# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN pip install --upgrade pip

# install modules from the requirements.txt
RUN pip install -r requirements.txt

# Run the python script
CMD [ "python3","AnimeDownloader.py" ]