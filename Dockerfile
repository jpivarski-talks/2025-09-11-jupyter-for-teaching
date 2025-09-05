# base image: Python 3.12 without much else
FROM python:3.12-slim

# copy the requirements file into the image
COPY requirements.txt .

# install all of the packages in the image (without a cache because we're only doing it once)
RUN pip install --no-cache-dir -r requirements.txt

# copy in some custom settings to control how Jupyter looks (Jupyter is the /root user in the container)
RUN mkdir -p /root/.jupyter/lab/user-settings/@jupyterlab/apputils-extension
COPY settings/* /root/.jupyter/lab/user-settings/@jupyterlab/apputils-extension

# let JupyterLab's network port be accessible outside of the container
EXPOSE 8888

# command to run when invoking this image: JupyterLab in the notebooks directory without running a web browser in the container
CMD ["jupyter", "lab", "--notebook-dir=./notebooks", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
