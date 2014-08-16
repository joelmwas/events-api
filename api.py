from flask import Flask, request
from flask.ext.restful import reqparse, abort, Resource, Api

app = Flask(__name__)
api = Api(app)

events = {
	'1': {'event': 'Mozilla Open Day', 'location': 'Mt. Kenya University, Mombasa'},
	'2': {'event': 'Open Data Day', 'location': 'Jomo Kenyatta University, Mombasa Campus'},
	'3': {'event': 'Google Barcamp', 'location': 'Lotus Hotel'},
}


def abort_if_event_doesnt_exist(event_id):
	if event_id not in events:
		abort(404, message="Event {} does not exit".format(event_id))

parser = reqparse.RequestParser()
parser.add_argument('event', type=str, required=True)
help="Event name cannot be blank"


class Event(Resource):
	""" Show a single event and allows you to delete """
	def get(self, event_id):
		abort_if_event_doesnt_exist(event_id)
		return events[event_id]

	def delete(self, event_id):
		abort_if_event_doesnt_exist(event_id)
		del events[event_id]
		return '', 204

	def put(self, event_id):
		args = parser.parse_args()
		event = {'event', args['event']}
		event[event_id] = event
		return event, 201
		

class EventList(Resource):
	""" Provide a list of events, POST and add new events. """ 
	
	def get(self):
		return events

	def post(self):
		args = parser.parse_args()
		event_id = 'event%d' % (len(events) + 1)
		events[event_id] = {'event': args['event']}
		return events[event_id], 201

# API routing
api.add_resource(EventList, '/api/events')
api.add_resource(Event, '/api/events/<string:event_id>')

if __name__ == '__main__':
    app.run()
