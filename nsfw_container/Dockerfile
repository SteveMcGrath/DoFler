FROM bvlc/caffe:cpu

COPY nsfw /opt/nsfw/
RUN pip install -r /opt/nsfw/requirements.txt

EXPOSE 8080

CMD python /opt/nsfw/nsfw.py