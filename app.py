from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123456@localhost/cargo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

if __name__ == '__main__':
  app.run(debug=True)


class Transport(db.Model):
    __tablename__ = 'cargo'
    id = db.Column(db.Integer, primary_key = True)
    transport_name = db. Column(db.String(100), nullable = False)
    transport_phone_number = db. Column(db.String(10), nullable = False)
    transport_truck_number = db. Column(db.String(8), nullable = False)
    transport_cargo_type = db.Column(db.String(50), nullable = False)
    transport_cargo_description = db.Column(db.String(400), nullable = False)
    transport_departure_time = db.Column(db.Date(), nullable = False)
    transport_departure_location = db.Column(db.String(100), nullable = False)
    transport_arrival_location = db.Column(db.String(100), nullable = False)
    transport_weight = db.Column(db.Integer, nullable = True)


    def __repr__(self):
        return "<Transport %r>" % self.transport_name


@app.route('/')
def index():
    return jsonify({"message":"Welcome to my Transport API"})


@cross_origin()
@app.route('/cargo', methods = ['POST'])
def create_transport():
    cargo_data = request.json

    transport_name = cargo_data['transport_name']
    transport_phone_number = cargo_data['transport_phone_number']
    transport_truck_number = cargo_data['transport_truck_number']
    transport_departure_time = cargo_data['transport_departure_time']
    transport_departure_location = cargo_data['transport_departure_location']
    transport_arrival_location = cargo_data['transport_arrival_location']
    transport_weight = cargo_data['transport_weight']
    transport_cargo_type = cargo_data['transport_cargo_type']

    transport_cargo_description = cargo_data['transport_cargo_description']
    transport = Transport(transport_name = transport_name , transport_phone_number = transport_phone_number,
    transport_truck_number = transport_truck_number, transport_departure_time = transport_departure_time,
    transport_departure_location = transport_departure_location, transport_arrival_location = transport_arrival_location,
    transport_weight = transport_weight, transport_cargo_type = transport_cargo_type, transport_cargo_description = transport_cargo_description)
    db.session.add(transport)
    db.session.commit()
    

    return jsonify({"success": True,"response":"Transport added"})


@cross_origin()    
@app.route('/gettransports', methods = ['GET'])
def get_transports():
     all_transports = []
     transports = Transport.query.all()
     for transport in transports:
          results = {
                    "id":transport.id,
                    "transport_name":transport.transport_name,
                    "transport_phone_number":transport.transport_phone_number,
                    "transport_truck_number":transport.transport_truck_number,
                    "transport_departure_time":transport.transport_departure_time,
                    "transport_departure_location":transport.transport_departure_location,
                    "transport_arrival_location":transport.transport_arrival_location,
                    "transport_weight":transport.transport_weight,
                    "transport_cargo_type":transport.transport_cargo_type,
                    "transport_cargo_description":transport.transport_cargo_description }
          all_transports.append(results)

     return jsonify(
            {
                "success": True,
                "transports": all_transports,
                "total_transports": len(transports),
            }
        )


@cross_origin()    
@app.route('/transports/<int:id>', methods = ['GET'])
def get_transport(id):
    transport = Transport.query.get(id)
    if transport is None:
        abort(404)
    else:
        result = {
                  "id":transport.id,
                  "transport_name":transport.transport_name,
                  "transport_phone_number":transport.transport_phone_number,
                  "transport_truck_number":transport.transport_truck_number,
                  "transport_departure_time":transport.transport_departure_time,
                  "transport_departure_location":transport.transport_departure_location,
                  "transport_arrival_location":transport.transport_arrival_location,
                  "transport_weight":transport.transport_weight,
                  "transport_cargo_type":transport.transport_cargo_type,
                  "transport_cargo_description":transport.transport_cargo_description }
        return jsonify(
                {
                "success": True,
                "transport": result,
                })


@cross_origin()  
@app.route("/transports/<int:id>", methods = ["PATCH"])
def update_transport(id):
    transport = Transport.query.get(id)
    if transport is None:
        abort(404)
    else:  
        cargo_data = request.json
        transport.transport_name = cargo_data['transport_name']
        transport.transport_phone_number = cargo_data['transport_phone_number']
        transport.transport_truck_number = cargo_data['transport_truck_number']
        transport.transport_departure_time = cargo_data['transport_departure_time']
        transport.transport_departure_location = cargo_data['transport_departure_location']
        transport.transport_arrival_location = cargo_data['transport_arrival_location']
        transport.transport_weight = cargo_data['transport_weight']
        transport.transport_cargo_type = cargo_data['transport_cargo_type']
        db.session.add(transport)
        db.session.commit()
        return jsonify({"success": True, "response": "Transport details updated"})


@app.route("/transports/<int:id>", methods = ["DELETE"])
def delete_transport(id):
    transport = Transport.query.get(id)
    if transport is None:
        abort(404)
    else:
        db.session.delete(transport)
        db.session.commit()
        return jsonify({"success": True, "response": "Transport deleted"})