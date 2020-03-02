import os
import peewee
import configparser
from peewee import *
from playhouse.pool import PooledMySQLDatabase

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
cf = configparser.ConfigParser()
cf.read(PATH('../homepage.config'))
DB_PASS = cf.get('config', 'DB_PASS')


class UnknownField(object):

    def __init__(self, *_, **__):
        pass


class BaseModel(Model):

    class Meta:
        database = PooledMySQLDatabase('PersonalHomepage', user='root', password=DB_PASS, host='localhost', port=3306)


class app(BaseModel):
    name = CharField()
    url = CharField()
    user_id = IntegerField()
    expect_price = IntegerField()
    order = IntegerField()
    is_valid = IntegerField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'app'


#用户表增加email和微信推送id的config


class app_price(BaseModel):
    app_id = IntegerField()
    price = CharField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'app_price'


class app_push(BaseModel):
    user_id = IntegerField()
    is_valid = IntegerField()
    notify = IntegerField()  # 是否需要推送 0:否,1:是
    notify_method = IntegerField()  # 1:微信,2:邮件
    notify_interval_raw = IntegerField()  # 用户填写的间隔
    notify_interval_unit = IntegerField()  # 用户选择的单位1:小时,2:天
    notify_interval = IntegerField()  # 转化成小时的间隔
    notify_trigger_time = DateTimeField()  #触发时间，小于此时间则触发通知
    update_time = DateTimeField()

    class Meta:
        table_name = 'app_push'


app.create_table()
app_price.create_table()
app_push.create_table()