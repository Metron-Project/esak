from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class Prices:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class PriceSchemas(Schema):
    printPrice = fields.Decimal(places=2, allow_none=True, attribute="print")
    digitalPurchasePrice = fields.Decimal(places=2, allow_none=True, attribute="digital")

    class Meta:
        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        return {d["type"]: d["price"] for idx, d in enumerate(data, 0) if d["type"][idx]}

    @post_load
    def make(self, data, **kwargs):
        return Prices(**data)
