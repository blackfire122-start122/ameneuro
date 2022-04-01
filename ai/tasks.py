# from ameneuro.celery import app

# from tensorflow.keras.datasets import mnist
# from tensorflow import keras
# from keras.applications.vgg16 import decode_predictions
# from PIL import Image
# import numpy as np
# import io
# import binascii
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# model = keras.applications.VGG16()
# channel_layer = get_channel_layer()

# @app.task
def recognize_task(img,username):
	img = Image.open(io.BytesIO(binascii.a2b_base64(img)))
	img = img.convert(mode='RGB')
	img = img.resize((224,224), Image.BILINEAR)
	img = np.array(img)

	x = keras.applications.vgg16.preprocess_input(img)
	x = np.expand_dims(x, axis=0)

	res = decode_predictions(model.predict(x),top=1)[0][0]

	try:
		async_to_sync(channel_layer.group_send)(
		"chat_"+username,{
			"type": "chat.message",
			"text": {'type':'recognize','recognize':res[1],'procent':str(res[2]*100)},
		})
		return "Good"
	except:return "Fail"