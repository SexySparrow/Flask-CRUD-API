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
    name = db. Column(db.String(100), nullable = False)
    phone_number = db. Column(db.String(10), nullable = False)
    truck_number = db. Column(db.String(8), nullable = False)
    cargo_type = db.Column(db.String(50), nullable = False)
    cargo_description = db.Column(db.String(400), nullable = False)
    departure_time = db.Column(db.Date(), nullable = False)
    departure_location = db.Column(db.String(100), nullable = False)
    arrival_location = db.Column(db.String(100), nullable = False)
    weight = db.Column(db.Integer, nullable = True)


    def __repr__(self):
        return "<Transport %r>" % self.name


@app.route('/')
def index():
    return jsonify({"message":"Welcome to my Transport API"})


@cross_origin()
@app.route('/cargo', methods = ['POST'])
def create_transport():
    cargo_data = request.json

    name = cargo_data['name']
    phone_number = cargo_data['phone_number']
    truck_number = cargo_data['truck_number']
    departure_time = cargo_data['departure_time']
    departure_location = cargo_data['departure_location']
    arrival_location = cargo_data['arrival_location']
    weight = cargo_data['weight']
    cargo_type = cargo_data['cargo_type']

    cargo_description = cargo_data['cargo_description']
    transport = Transport(name =name ,phone_number =phone_number,
    truck_number =truck_number,departure_time =departure_time,
    departure_location =departure_location,arrival_location =arrival_location,
    weight =weight,cargo_type =cargo_type,cargo_description =cargo_description)
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
                    "name":transport.name,
                    "phone_number":transport.phone_number,
                    "truck_number":transport.truck_number,
                    "departure_time":transport.departure_time,
                    "departure_location":transport.departure_location,
                    "arrival_location":transport.arrival_location,
                    "weight":transport.weight,
                    "cargo_type":transport.cargo_type,
                    "cargo_description":transport.cargo_description }
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
                  "name":transport.name,
                  "phone_number":transport.phone_number,
                  "truck_number":transport.truck_number,
                  "departure_time":transport.departure_time,
                  "departure_location":transport.departure_location,
                  "arrival_location":transport.arrival_location,
                  "weight":transport.weight,
                  "cargo_type":transport.cargo_type,
                  "cargo_description":transport.cargo_description }
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
        transport.name = cargo_data['name']
        transport.phone_number = cargo_data['phone_number']
        transport.truck_number = cargo_data['truck_number']
        transport.departure_time = cargo_data['departure_time']
        transport.departure_location = cargo_data['departure_location']
        transport.arrival_location = cargo_data['arrival_location']
        transport.weight = cargo_data['weight']
        transport.cargo_type = cargo_data['cargo_type']
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