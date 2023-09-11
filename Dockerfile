# Use the specified jupyter/scipy-notebook image as the base
FROM jupyter/scipy-notebook:x86_64-0d324bc0b38c

# Set working directory in the container
WORKDIR /home/jovyan/work

# Clone the git repository
RUN git clone https://github.com/bensonbs/SQL_Docker

# Change directory to the cloned repo
WORKDIR /home/jovyan/work/SQL_Docker/work

# Run the install script
RUN sh install.sh

# Expose any necessary ports (e.g., for Jupyter)
EXPOSE 8888

# Specify the default command to run on container start
CMD ["start-notebook.sh"]
