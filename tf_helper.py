'''
	Tensorflow serving grpc client helper function for inference.
'''


import grpc
import numpy as np
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc


def get_stub(host, port='8500'):
	channel = grpc.insecure_channel(f'{host}:{port}')
	stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
	return stub

def get_model_prediction(model_input, stub, model_name='image_classifier', signature_name='serving_default'):

	
	class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
	im = (model_input/255)
	im = np.expand_dims(im, axis=0)
	
	print("Image shape: ",im.shape)
	# We will be using Prediction Task so it uses predictRequest function from predict_pb2
	
	request = predict_pb2.PredictRequest()
	request.model_spec.name = model_name
	request.model_spec.signature_name = signature_name
	request.inputs['Conv1_input'].CopyFrom(tf.make_tensor_proto(im, dtype = tf.float32))
	
	response = stub.Predict.future(request, 5.0)
	output = response.result().outputs['Dense']
	output_shape = [dim.size for dim in output.tensor_shape.dim]

	# convert bytes to numpy array
	output_np = np.array(output.float_val).reshape(output_shape)
	label = class_names[np.argmax(output_np)]
	
	return label



