ARG VARIANT=3.10-bullseye

FROM python:${VARIANT}

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

WORKDIR /workspace

RUN apt-get update \
  && apt-get install -y apt-utils sudo \
  && groupadd --gid ${USER_GID} ${USERNAME} \
  && useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} \
  && echo ${USERNAME} ALL=\(ALL:ALL\) NOPASSWD: ALL >/etc/sudoers.d/${USERNAME} \
  && chmod 0440 /etc/sudoers.d/${USERNAME} \
  && apt-get autoremove -y \
  && apt-get clean -y

USER ${USERNAME}
RUN echo "[ -f /workspace/.devcontainer/bash_aliases ] && . /workspace/.devcontainer/bash_aliases" >>/home/${USERNAME}/.bashrc
