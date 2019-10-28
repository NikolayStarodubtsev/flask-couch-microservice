import couchdb
import os
import flask
import bcrypt


class CouchProvider(object):
    def __init__(self):
        self.admin_username = os.environ.get("admin_username") or "admin"
        self.admin_password = os.environ.get("admin_password") or "pass"
        self.server_url = os.environ.get('server_url') or "127.0.0.1"
        couchdb_url = 'http://{}:{}@{}'.format(self.admin_username,
                                               self.admin_password,
                                               self.server_url)
        self.couch = couchdb.Server(couchdb_url)
        self.hashed = bcrypt.hashpw(self.admin_password.encode('utf8'),
                                    bcrypt.gensalt())

    def create_product(self, payload):
        # Step 1; Check if the auth header has been provided
        if 'Authorization' not in flask.request.headers:
            return {"error": "Not correctly authorized"}, 401
        # Step 2; Check the password provided by the user.
        if bcrypt.hashpw(flask.request.authorization.password.encode('utf8'),
                         self.hashed) == self.hashed:
            couch = couchdb.Server('http://{}:{}@{}'.format(
                self.admin_username,
                flask.request.authorization.password,
                self.server_url))
            db = couch['products']
            if payload['_id'] in db:
                return {"error": "Found product with existing ID"}, 409
            else:
                db.save(payload)
                return payload, 201

    def read_product(self, prod_id) -> str:
        db = self.couch['products']
        if(prod_id in db):
            product = db[prod_id]
            return product, 200
        else:
            return {"error": "Product not found"}, 400

    def update_product(self, payload):
        # Step 1; Check if the auth header has been provided
        if 'Authorization' not in flask.request.headers:
            return {"error": "Not correctly authorized"}, 401
        # Step 2; Check the password provided by the user.
        if bcrypt.hashpw(flask.request.authorization.password.encode('utf8'),
                         self.hashed) == self.hashed:
            couch = couchdb.Server('http://{}:{}@{}'.format(
                self.admin_username,
                flask.request.authorization.password,
                self.server_url))
            db = couch['products']  # Select our db
            if payload['_id'] in db:  # Check if product exists in DB
                print("Found a product in DB with this _id")
                doc = db[payload['_id']]
                # Add the docs _rev prop to the payload or a conflict will occur
                payload['_rev'] = doc['_rev']
                db.save(payload)  # Save the new details
                return {"message": "Success"}, 201
            else:
                # Product not found
                return {"error": "Product not found"}, 409
        else:
            # Reaching here means the provided password was not valid
            print("It does not match")
            return {"error": "Not correctly authorized"}, 401

    def delete_product(self, id):
        # Step 1; Check if the auth header has been provided
        if 'Authorization' not in flask.request.headers:
            return {"error": "Not correctly authorized"}, 401
        # Step 2; Check the password provided by the user.
        if bcrypt.hashpw(flask.request.authorization.password.encode('utf8'),
                         self.hashed) == self.hashed:
            couch = couchdb.Server(os.environ['server_url'])
            print("It matches")
            try:
                db = couch['products']
                prod_to_delete = db[id]
                db.delete(prod_to_delete)
                return {"message": "Success"}, 200
            except Exception:
                return {"error": "Product not found"}, 400

        else:
            # Reaching here means the provided password was not valid
            print("It does not match")
            return {"error": "Not correctly authorized"}, 401
