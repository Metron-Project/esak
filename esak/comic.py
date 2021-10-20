from marshmallow import INCLUDE, Schema, fields, post_load, pre_load

from . import character, creator, dates, events, exceptions, prices, series, urls


class Comic:
    def __init__(self, **kwargs):
        if "response" not in kwargs:
            kwargs["response"] = None

        for k, v in kwargs.items():
            setattr(self, k, v)


class ComicSchema(Schema):
    id = fields.Int()
    digitalId = fields.Int(attribute="digital_id")
    title = fields.Str()
    issueNumber = fields.Int(attribute="issue_number")
    variantDescription = fields.Str(attribute="variant_description")
    description = fields.Str(allow_none=True)
    modified = fields.DateTime()
    isbn = fields.Str()
    upc = fields.Str()
    diamondCode = fields.Str(attribute="diamond_code")
    ean = fields.Str()
    issn = fields.Str()
    format = fields.Str()
    pageCount = fields.Int(attribute="page_count")
    # textObjects
    resourceURI = fields.Url(attribute="resource_uri")
    urls = fields.Nested(urls.UrlsSchema)
    series = fields.Nested(series.SeriesSchema)
    # variants
    # collections
    # collectedIssues
    dates = fields.Nested(dates.DatesSchema)
    prices = fields.Nested(prices.PriceSchemas, allow_none=True)
    # thumbnail
    images = fields.List(fields.Url)
    creators = fields.Nested(creator.CreatorsSchema, many=True)
    characters = fields.Nested(character.CharactersSchema, many=True)
    # stories
    events = fields.Nested(events.EventsSchema, many=True)

    class Meta:
        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        if data.get("code", 200) != 200:
            raise exceptions.ApiError(data.get("status"))

        if "status" in data:
            data["data"]["results"][0]["response"] = data
            data = data["data"]["results"][0]

        # Marvel comic 1768, and maybe others, returns a modified of
        # "-0001-11-30T00:00:00-0500". The best way to handle this is
        # probably just to ignore it, since I don't know how to fix it.
        if data.get("modified", " ")[0] == "-":
            del data["modified"]

        if "events" in data:
            data["events"] = data["events"]["items"]

        if "creators" in data:
            data["creators"] = data["creators"]["items"]

        if "characters" in data:
            data["characters"] = data["characters"]["items"]

        if "images" in data:
            data["images"] = [
                "{}.{}".format(img["path"], img["extension"]) for img in data["images"]
            ]

        if "isbn" in data:
            data["isbn"] = str(data["isbn"])

        if "diamondCode" in data:
            data["diamondCode"] = str(data["diamondCode"])

        return data

    @post_load
    def make(self, data, **kwargs):
        return Comic(**data)
