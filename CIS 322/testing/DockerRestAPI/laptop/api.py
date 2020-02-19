from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Laptop(Resource):
    def get(self):
        return {
            'Laptops': ['Mac OS', 'Dell', 
            'Windozzee',
	    'Yet another laptop!'
            ]
        }

api.add_resource(Laptop, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
