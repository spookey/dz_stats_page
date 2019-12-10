from logging import getLogger

from sqlalchemy.ext.declarative import declared_attr

from stats.start.extensions import DB

LOG = getLogger(__name__)

# pylint: disable=no-member
# pylint: disable=too-few-public-methods


class CRUDMixin:

    @classmethod
    def create(cls, _commit=True, **kwargs):
        LOG.info('creating model "%s"', cls.__name__)

        inst = cls(**kwargs)
        return inst.save(_commit=_commit)

    def update(self, _commit=True, **kwargs):
        LOG.info('updating model "%s"', self.__class__.__name__)

        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if _commit:
            return self.save(_commit=_commit)
        return self

    def save(self, _commit=True):
        LOG.info('saving model "%s"', self.__class__.__name__)

        DB.session.add(self)
        if _commit:
            DB.session.commit()
        return self

    def delete(self, _commit=True):
        LOG.info('deleting model "%s"', self.__class__.__name__)

        DB.session.delete(self)
        if _commit:
            DB.session.commit()
        return True


class NameMixin:
    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()


class PrimeMixin:
    prime = DB.Column(DB.Integer(), primary_key=True)

    @classmethod
    def by_prime(cls, value):
        if any([
                isinstance(value, (bytes, str)) and value.isdigit(),
                isinstance(value, (float, int))
        ]):
            return cls.query.get(int(value))
        return None


class BaseModel(CRUDMixin, NameMixin, DB.Model):
    __abstract__ = True


class Model(PrimeMixin, BaseModel):
    __abstract__ = True
