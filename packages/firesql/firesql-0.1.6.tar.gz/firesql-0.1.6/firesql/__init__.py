import datetime
from typing import Any
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import mode
from sqlalchemy.sql.schema import ForeignKey
import os
from functools import reduce


class Float(Float):
    pass


class Column(Column):
    pass


class Integer(Integer):
    pass


class String(String):
    pass


class DateTime(DateTime):
    pass


class Boolean(Boolean):
    pass


class ForeignKey(ForeignKey):
    pass


class FiresqlBase():
    def begin(self):
        return declarative_base()


or_ = sqlalchemy.sql.or_
and_ = sqlalchemy.sql.and_


class dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class NewSesion(sessionmaker):

    def add(self, instance):
        super.begin_nested()
        super.add(instance)

    def commit(self):
        super.commit()

    def close(self):
        super.close()

    def delete(self, instance):
        super.delete(instance)

    def rollback(self):
        super.rollback()

    def query(self, *args):
        super.query(**args)


class ErrorGetData(Exception):
    pass


class ErrorFilterData(Exception):
    def __init__(self, value):
        message = f"Got an incorrect filter list {value}"
        super().__init__(message)


class FilterSingledRead():
    value: Any
    type: str
    name: str

    def __init__(self, my_dict, name):
        self.name = name
        for key in my_dict:
            setattr(self, key, my_dict[key])


class Firesql(object):
    conn: engine

    def connect_sql(self, host_name: str, user_name: str, user_password: str, db_name: str, port=3306):
        try:
            self.conn = create_engine(
                f"mysql+pymysql://{user_name}:{user_password}@{host_name}:{port}/{db_name}")
            # Set environment variables
            os.environ['DATABASE_URL'] = "mysql+pymysql://{user_name}:{user_password}@{host_name}:{port}/{db_name}"
            self.metadata = MetaData(self.conn)
            print("Connection to MySQL DB successful")
        except Exception as e:
            print(f"The error '{e}' occurred")

    def create_all(self, base):
        base.metadata.create_all(self.conn)

    def drop_all(self, base):
        base.metadata.drop_all(self.conn)

    def session(self):
        Sess = NewSesion(bind=self.conn)
        session: NewSesion = Sess()
        return session

    def singled_read(
        self,
        model,
        page=0,
        page_size=50,
        filters=None,
        type_class=True,
        data_filter: dict = {},
        or_join=False,
        order_by=None,
        ascendent=True,
    ):
        session = self.session()
        query = session.query(model)

        if data_filter:
            filter_data = self.validate_data_singled_read(
                model, data_filter, or_join)
            query = query.filter(filter_data)
        if filters is not None:
            query = query.filter(filters)
        total_count = query.count()
        if order_by is not None:
            order = getattr(model, order_by).asc(
            ) if ascendent else getattr(model, order_by).desc()
            query = query.order_by(order)
        if page_size > 0:
            query = query.limit(page_size)
        if page > 0:
            query = query.offset(page * page_size)
        data: list[type[model]] = query.all()
        if not type_class:
            list_data = list(map(lambda x: x.__dict__, data))
            return list(map(self.iterdict, list_data)), total_count
        return data, total_count

    def validate_data_singled_read(self, model, filter_data: dict, or_join=False):
        values_in_model = dir(model)
        get_filter_data = list(filter_data.keys())
        if not set(get_filter_data).issubset(set(values_in_model)):
            raise ErrorFilterData(get_filter_data)
        filter = []

        def get_filter(filter, type: str, value):
            if type == 'like':
                return getattr(filter, 'ilike')("%{}%".format(value))
            elif type == 'equal':
                return filter == value
            elif type == 'higher':
                return filter > value
            elif type == 'lowwer':
                return filter < value
            else:
                return None
        for key in filter_data.keys():
            new_filter_data = FilterSingledRead(filter_data[key], key)
            new_filter = getattr(model, new_filter_data.name)
            filter_type = get_filter(
                new_filter, new_filter_data.type, new_filter_data.value)
            if filter_type is not None:
                filter.append(filter_type)
        if or_join:
            return or_(*filter)
        return and_(*filter)

    def iterdict(self, d):
        for k, v in d.items():
            if isinstance(v, dict):
                self.iterdict(v)
            else:
                if type(v) == datetime.datetime:
                    v = str(v)
                d.update({k: v})
        return d
