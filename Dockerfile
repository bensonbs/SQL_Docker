# Use the specified jupyter/scipy-notebook image as the base
FROM jupyter/scipy-notebook:x86_64-0d324bc0b38c

# Set working directory in the container
WORKDIR /home/jovyan

# Clone the git repository
RUN git clone https://github.com/bensonbs/SQL_Docker

RUN chmod -R 777 SQL_Docker

# Change directory to the cloned repo
WORKDIR /home/jovyan/SQL_Docker/scripts

# Run the install script
USER root
RUN apt-get update -y
RUN apt-get install -y lsb-release
RUN apt-get install -y curl
RUN bash setup.sh
RUN pip install pyodbc

WORKDIR /home/jovyan

RUN rm -rf SQL_Docker
# Expose any necessary ports (e.g., for Jupyter)
EXPOSE 8888

# Specify the default command to run on container start
CMD ["start-notebook.sh"]
