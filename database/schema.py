from datetime import datetime

from peewee import AutoField, CharField, DateField, DateTimeField, FloatField, ForeignKeyField, Model, SqliteDatabase

import config as cfg

db = SqliteDatabase(cfg.DB_NAME)


class BaseModel(Model):
    class Meta:
        database = db


class Region(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(unique=True)


class MetricCategory(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(unique=True)


class Metric(BaseModel):
    id = AutoField(primary_key=True)
    category = ForeignKeyField(MetricCategory, backref='metrics')
    name = CharField()


class MonthlyData(BaseModel):
    id = AutoField(primary_key=True)
    region = ForeignKeyField(Region)
    metric = ForeignKeyField(Metric)
    value = FloatField(null=True)
    metric_date = DateField()
    created_date = DateTimeField(default=datetime.now)
