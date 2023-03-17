import whisper


class Transcriber(object):

	def __init__(self, language='english', model_size='base'):
		self.language = language.lower()
		self.model_size = model_size.lower()
		self.model_name = self.model_size
		if language == 'english' and self.model_size != 'large':
		  self.model_name += '.en'
		self.model = whisper.load_model(self.model_name)

	def __call__(self, path):
		result = self.model.transcribe(path)
		return result