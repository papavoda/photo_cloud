# Pull base image
FROM python:3.10-alpine

# Set environment
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x entrypoint.sh

# Copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
