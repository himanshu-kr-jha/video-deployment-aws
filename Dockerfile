FROM python:3.9

COPY process_video.py .
COPY requirements.txt .

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y ffmpeg \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

ENTRYPOINT python process_video.py \
    --input_bucket=${INPUT_BUCKET} \
    --input_filepath=${INPUT_FILEPATH} \
    --output_bucket=${OUTPUT_BUCKET} \
    --output_filepath=${OUTPUT_FILEPATH}