ARG VARIANT=3.10-bullseye

FROM python:${VARIANT}

ARG USERNAME=vscode USER_UID=1000
ARG USER_GID=${USER_UID}
RUN groupadd --gid ${USER_GID} ${USERNAME} \
  && useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME}

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

USER ${USERNAME}

ENTRYPOINT [ "python", "manage.py", "runserver" ]
CMD [ "0.0.0.0:3109" ]
EXPOSE 3109
