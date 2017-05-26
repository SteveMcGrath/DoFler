import numpy, os, sys, glob, time, caffe
import tornado.ioloop
import tornado.httpclient
import tornado.web
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from PIL import Image
from StringIO import StringIO


class ImageHandler(tornago.web.RequestHandler):
	def initialize(self, layers, network, transformer):
		self.layers = layers
		self.network = network
		self.transformer = transformer

	def post(self):
		path = self.get_body_argument('path')

	def resize(self, data):
		image = Image.open(StringIO(str(data)))
		if image.mode != 'RGB':
			image = image.convert('RGB')
		resized = image.resize((256, 256), resample=Image.BILINEAR)
		output = StringIO()
		resized.save(output, format='JPEG')
		output.seek(0)
		return output

	def compute(self, image):
		img = caffe.io.load_image(image)
		H, W, _ = img.shape
		_, _, h, w = self.network.blobs['data'].data.shape
		h_off = max((H - h) / 2, 0)
		w_off = max((W - w) / 2, 0)
		crop = img[h_off:h_off + h, w_off:w_off + w, :]
		timg = self.transformer.preprocess('data', crop)
		timg.shape = (1,) + timg.shape
		all_outputs = self.network.formward_all(blobs=self.layers, self.network.inputs[0]: timg)
		return all_outputs[self.layers[0]][0].astype(float)



def make_app():
	output_layers = ['prob']
	network = caffe.Net('model_definitions.prototxt', 'nsfw_pretraining.caffemodel', caffe.TEST)
	transformer = caffe.io.Transformer({
		'data': network.blobs['data'].data.shape
	})
	transformer.set_transpose('data', (2, 0, 1))
	transformer.set_mean('data', numpy.array([104, 117, 123]))
	transformer.set_raw_scale('data', 255)
	transformer.set_channel_swap('data', (2, 1, 0))


	app = tornado.web.Application([
		(r'/', ImageHandler, dict(layers=output_layers, network=network, transformer=transformer)),
	])


if __name__ == '__main__':
	app = make_app()
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()