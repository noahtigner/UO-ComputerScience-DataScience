FROM python:3-onbuild

# Copying source in current directory into the image
# python:3-onbuild expects the source in /usr/src/app
COPY . /usr/src/app

# Commands in a list
CMD ["python", "api.py"]
