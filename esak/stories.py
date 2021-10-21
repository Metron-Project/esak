from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class StorySummary:
    def __init__(self, id=None, name=None, type=None, **kwargs):
        self.id = id
        self.name = name
        self.type = type
        self.unknown = kwargs


class StorySummarySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    type = fields.Str()

    class Meta:
        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        data["id"] = data["resourceURI"].split("/")[-1]
        return data

    @post_load
    def make(self, data, **kwargs):
        return StorySummary(**data)
