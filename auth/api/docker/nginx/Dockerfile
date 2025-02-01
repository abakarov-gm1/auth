FROM nginx:latest
WORKDIR /app
RUN apt-get update
RUN apt-get install git -y
RUN apt-get install certbot python3-certbot-nginx -y

RUN apt install -y locales && sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG=ru_RU.UTF-8
ENV LANGUAGE=ru_RU:UTF-8
ENV LC_ALL=ru_RU.UTF-8
