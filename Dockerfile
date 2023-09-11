# Use the specified jupyter/scipy-notebook image as the base
FROM jupyter/scipy-notebook:x86_64-0d324bc0b38c

# Set working directory in the container
WORKDIR /home/jovyan

# Clone the git repository
RUN git clone https://github.com/bensonbs/SQL_Docker

# Change directory to the cloned repo
WORKDIR /home/jovyan/SQL_Docker

# Run the install script
RUN sh /home/jovyan/SQL_Docker/install.sh

WORKDIR /home/jovyan
# Expose any necessary ports (e.g., for Jupyter)
EXPOSE 8888

# Specify the default command to run on container start
CMD ["start-notebook.sh"]
