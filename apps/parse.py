from lively import settings

__author__ = 'aamish'
import json, http.client, urllib
from parse_rest.datatypes import Object


#Parse Models for ParsePy
class Gro(Object):
    pass


class ParseHelper():

    #initial methods *********************************************************************

    def __init__(self):
        self.connection = http.client.HTTPSConnection('api.parse.com', 443)
        self.connection.connect()

    def make_request(self, method, content_type, request_url, request_data):
        self.connection.request(
            method,
            request_url,
            request_data,
            {
                "X-Parse-Application-Id": settings.APPLICATION_ID,
                "X-Parse-REST-API-Key": settings.REST_API_KEY,
                "Content-Type": content_type
            }
        )

        return json.loads(self.connection.getresponse().read().decode('utf-8'))

    #item methods *********************************************************************

    def item_add(self, obj, password):
        response = self.make_request('POST', "application/json", '/1/classes/Gro', json.dumps({
                "first_name": obj.user.first_name,
                "last_name": obj.user.last_name,
                "username": obj.user.username,
                "password": password,
                "gro_id": obj.user.id,
                "branch_id": obj.branch_id,
            })
        )
        return response['objectId']

    def item_update(self, obj, new_password):
        if new_password:
            response = self.make_request('PUT', "application/json", '/1/classes/Gro/%s' % obj.objectId, json.dumps({
                    "first_name": obj.user.first_name,
                    "last_name": obj.user.last_name,
                    "username": obj.user.username,
                    "password": new_password,
                    "gro_id": obj.user.id,
                    "branch_id": obj.branch_id,
                })
            )
        else:
            response = self.make_request('PUT', "application/json", '/1/classes/Gro/%s' % obj.objectId, json.dumps({
                    "first_name": obj.user.first_name,
                    "last_name": obj.user.last_name,
                    "username": obj.user.username,
                    "gro_id": obj.user.id,
                    "branch_id": obj.branch_id,
                })
            )
        return response