import json


class CustJSONEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            json.JSONEncoder.default(self, o)
        except TypeError:
            try:
                return o.to_serializable()
            except AttributeError:
                raise TypeError(repr(o) + " is not JSON serializable and doesn't have .to_serializable()")
