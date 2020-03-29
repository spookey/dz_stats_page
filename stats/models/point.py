from sqlalchemy.ext.hybrid import hybrid_property

from stats.database import CreatedMixin, Model
from stats.lib.clock import is_outdated
from stats.start.environment import BACKLOG_DAYS
from stats.start.extensions import DB

# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class Point(CreatedMixin, Model):
    value = DB.Column(DB.Float(), nullable=False)

    sensor_prime = DB.Column(
        DB.Integer(), DB.ForeignKey('sensor.prime'), nullable=False
    )

    @hybrid_property
    def outdated(self):
        return is_outdated(self.created, BACKLOG_DAYS)

    @classmethod
    def query_outdated(cls, query=None):
        query = query if query is not None else cls.query
        return query.filter(cls.outdated)
