#!/usr/bin/env python3
from flask_classful import FlaskView
from flask import request, abort, jsonify
from utils import json_required
from flask_jwt_simple import jwt_required, get_jwt_identity
from flask_influxdb import InfluxDB
from tzlocal import get_localzone
from datetime import datetime
from marshmallow.exceptions import ValidationError

from schemas import RecordSchema


class RecordView(FlaskView):
    influx_db = InfluxDB()
    record_schema = RecordSchema()

    @staticmethod
    def _transform_datapoints(hostname: str, timestamp: str, data: dict) -> list:
        datapoints = []

        for k, v in data.items():
            if k in ['entities', 'players']:

                for sk, sv in v.items():
                    datapoints.append({
                        "measurement": k,
                        "time": timestamp,
                        "tags": {
                            "host": hostname,
                            "world": sk
                        },
                        "fields": {
                            k: sv
                        }
                    })

            else:
                datapoints.append({
                    "measurement": k,
                    "time": timestamp,
                    "tags": {
                        "host": hostname
                    },
                    "fields": v
                })

        return datapoints

    @jwt_required
    @json_required
    def post(self):

        hostname = get_jwt_identity()
        timestamp = datetime.now(get_localzone()).isoformat()

        try:
            record = self.record_schema.load(request.get_json())
        except ValidationError as e:
            abort(422, str(e))

        self.influx_db.connection.write_points(
            self._transform_datapoints(hostname, timestamp, record)
        )

        return jsonify(record), 201
