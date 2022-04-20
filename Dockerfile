ARG VARIANT=3.10-bullseye

FROM python:${VARIANT}

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

WORKDIR /usr/src/app
COPY requirements.txt .
RUN groupadd --gid ${USER_GID} ${USERNAME} \
  && useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} \
  && pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . .

USER ${USERNAME}
ENTRYPOINT ["./entrypoint.sh"]
CMD ["0.0.0.0:3109"]
EXPOSE 3109
