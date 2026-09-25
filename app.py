from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


def find_event(event_id):
    """Helper to look up an event by id, or return None."""
    return next((e for e in events if e.id == event_id), None)


def next_id():
    """Generate the next available id (max existing id + 1, or 1 if empty)."""
    return max((e.id for e in events), default=0) + 1


# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)

    if not data or "title" not in data or not str(data["title"]).strip():
        return jsonify({"error": "A non-empty 'title' field is required"}), 400

    new_event = Event(next_id(), data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# PATCH /events/<id> - Update the title of an event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404

    data = request.get_json(silent=True)
    if not data or "title" not in data or not str(data["title"]).strip():
        return jsonify({"error": "A non-empty 'title' field is required"}), 400

    event.title = data["title"]
    return jsonify(event.to_dict()), 200


# DELETE /events/<id> - Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404

    events.remove(event)
    return jsonify({"message": f"Event {event_id} deleted successfully"}), 200


# GET /events - bonus helper so you can easily see current state while testing
@app.route("/events", methods=["GET"])
def list_events():
    return jsonify([e.to_dict() for e in events]), 200


if __name__ == "__main__":
    app.run(debug=True)