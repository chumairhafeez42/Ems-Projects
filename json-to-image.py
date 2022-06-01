import base64
import json

ENCODING = 'utf-8'

class JsonImageConverter:


    def __init__(self, filepath):
        self.jsonfile = filepath
        self.imagefile = f"{filepath.rsplit('.', 1)[0]}.png"


    def json_to_image(self):
        with open(self.jsonfile) as jsonfile:
            data = json.load(jsonfile)
            datastr = json.dumps(data)
            encoded = base64.urlsafe_b64encode(datastr.encode(ENCODING))  #1 way
            with open(self.imagefile, "wb") as fh:
                fh.write(encoded)


    def image_to_json(self):
        with open(self.imagefile, "rb") as image_file:
            encoded_string = base64.b64decode(image_file.read())
            data = encoded_string.decode(ENCODING)
            with open(self.jsonfile, 'w') as json_file:
                json.dump(json.loads(data), json_file)

if __name__ == '__main__':

    # json_to_image('test1.json')
    image_object = JsonImageConverter('test1.json')
    image_object.json_to_image()



