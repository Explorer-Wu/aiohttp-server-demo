import yaml

def load_config(path):
	with open(path, 'rt') as file:
    # yaml.full_load(file)
		config = yaml.safe_load(file)
		# config = yaml.load(file, Loader=yaml.Loader)
	return config

async def on_shutdown(app):
	print('=======================')
	for ws in app['websockets'].values():
		await ws.close(code=WSCloseCode.GOING_AWAY, message='Server shutdown')
	app['websockets'].clear()