#!/usr/bin/env python3
from marshmallow import Schema, fields
from marshmallow.validate import Range


class TPSSchema(Schema):
    # We are going to set 21 here, because paper occasionally report a little higher than 20
    v1m = fields.Float(data_key="1m", validate=Range(min=0, max=21), required=True)
    v5m = fields.Float(data_key="5m", validate=Range(min=0, max=21), required=True)
    v15m = fields.Float(data_key="15m", validate=Range(min=0, max=21), required=True)


class RAMSchema(Schema):
    heap_used = fields.Integer(validate=Range(min=0), required=True)  # Disallow negative
    non_heap_used = fields.Integer(validate=Range(min=0), required=True)


class RecordSchema(Schema):
    entities = fields.Dict(keys=fields.String(), values=fields.Integer(), allow_none=True, required=False)
    players = fields.Dict(keys=fields.String(), values=fields.Integer(), allow_none=True, required=False)
    ram = fields.Nested(RAMSchema, many=False, allow_none=True, required=False)
    tps = fields.Nested(TPSSchema, many=False, allow_none=True, required=False)
