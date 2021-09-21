FROM deezer/spleeter:3.6-5stems
RUN pip install boto3
WORKDIR /usr/scripts

COPY io_handler.py /usr/scripts

ENTRYPOINT ["python3", "io_handler.py"]

CMD ["arg1", "arg2"]