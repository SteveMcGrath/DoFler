FROM bvlc/caffe:cpu

COPY nsfw /opt/nsfw/
RUN mkdir /images
RUN pip install -r /opt/nsfw/requirements.txt

EXPOSE 8080

CMD python /opt/nsfw/nsfw.py