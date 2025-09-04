IMAGE_NAME=2025-09-11-jupyter-for-teaching

# build command makes an image with a unique name
build:
	docker build -t $(IMAGE_NAME) .

# run command depends on build,
# forwards JupyterLab's network port to your computer (outside the container), and
# links the in-container /notebooks directory to the outside-of-container ./notebooks directory
run: build
	docker run -p 127.0.0.1:8888:8888 -v "./notebooks:/notebooks" $(IMAGE_NAME)
