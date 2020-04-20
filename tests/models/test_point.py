from datetime import datetime

from pytest import mark

from observatory.models.mapper import EnumConvert, EnumHorizon
from observatory.models.point import Point
from observatory.models.sensor import Sensor
from observatory.start.environment import FMT_STRFTIME


@mark.usefixtures('session')
class TestPoint:

    @staticmethod
    def test_default_fields(gen_sensor):
        value = 23.5
        start = datetime.utcnow()
        sensor = gen_sensor()

        point = Point.create(sensor=sensor, value=value)

        assert point.sensor == sensor
        assert point.value == value
        assert start <= point.created
        assert point.created <= datetime.utcnow()

        assert point.created_epoch > 0
        assert point.created_epoch_ms > 0
        assert point.outdated is False

    @staticmethod
    def test_epochs(gen_sensor):
        point = Point.create(sensor=gen_sensor(), value=0)

        assert point.created_epoch <= (
            point.created - datetime.utcfromtimestamp(0)
        ).total_seconds()
        assert point.created_epoch_ms == 1000 * point.created_epoch

    @staticmethod
    def test_created_fmt(gen_sensor):
        sensor = gen_sensor()
        point = Point.create(sensor=sensor, value=42)
        assert point.created_fmt == point.created.strftime(FMT_STRFTIME)

    @staticmethod
    def test_delete_cascade(gen_sensor):
        sensor = gen_sensor()
        point = Point.create(sensor=sensor, value=23.5)

        assert Sensor.query.all() == [sensor]
        assert sensor.points == [point]
        assert Point.query.all() == [point]

        assert point.delete()

        assert Sensor.query.all() == [sensor]
        assert sensor.points == []
        assert Point.query.all() == []

    @staticmethod
    def test_outdated(gen_sensor, gen_points_batch):
        sensor = gen_sensor()
        olds, news, _ = gen_points_batch(sensor, old=1, new=1)

        assert olds[-1].outdated is True
        assert news[-1].outdated is False

    @staticmethod
    def test_query_outdated(gen_sensor, gen_points_batch):
        sensor = gen_sensor()
        olds, _, complete = gen_points_batch(sensor)

        assert Point.query.all() == complete
        assert Point.query_outdated().all() == olds

    @staticmethod
    def test_convert(gen_sensor):
        sensor = gen_sensor()
        neg = sensor.append(-23.5)
        nil = sensor.append(0)
        pos = sensor.append(13.37)

        for horizon, convert, numeric, params in [
                (None, None, False, (
                    (neg, -23.5), (nil, 0.0), (pos, 13.37),
                )),
                (None, None, True, (
                    (neg, -23.5), (nil, 0.0), (pos, 13.37),
                )),
                (EnumHorizon.NORMAL, EnumConvert.NATURAL, False, (
                    (neg, -23.5), (nil, 0.0), (pos, 13.37),
                )),
                (EnumHorizon.NORMAL, EnumConvert.NATURAL, True, (
                    (neg, -23.5), (nil, 0.0), (pos, 13.37),
                )),
                (EnumHorizon.INVERT, EnumConvert.NATURAL, False, (
                    (neg, 23.5), (nil, 0.0), (pos, -13.37),
                )),
                (EnumHorizon.INVERT, EnumConvert.NATURAL, True, (
                    (neg, 23.5), (nil, 0.0), (pos, -13.37),
                )),
                (EnumHorizon.NORMAL, EnumConvert.INTEGER, False, (
                    (neg, -23), (nil, 0), (pos, 13),
                )),
                (EnumHorizon.NORMAL, EnumConvert.INTEGER, True, (
                    (neg, -23), (nil, 0), (pos, 13),
                )),
                (EnumHorizon.INVERT, EnumConvert.INTEGER, False, (
                    (neg, 23), (nil, 0), (pos, -13),
                )),
                (EnumHorizon.INVERT, EnumConvert.INTEGER, True, (
                    (neg, 23), (nil, 0), (pos, -13),
                )),
                (EnumHorizon.NORMAL, EnumConvert.BOOLEAN, False, (
                    (neg, True), (nil, False), (pos, True),
                )),
                (EnumHorizon.NORMAL, EnumConvert.BOOLEAN, True, (
                    (neg, 1), (nil, 0), (pos, 1),
                )),
                (EnumHorizon.INVERT, EnumConvert.BOOLEAN, False, (
                    (neg, True), (nil, False), (pos, True),
                )),
                (EnumHorizon.INVERT, EnumConvert.BOOLEAN, True, (
                    (neg, -1), (nil, 0), (pos, -1),
                )),
        ]:
            for point, expect in params:
                assert point.convert(
                    horizon, convert, numeric=numeric
                ) == expect
