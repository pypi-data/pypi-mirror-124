# -*- coding: utf-8 -*-

"""Description: There are two main purpose of this module:
1. provide sqlalchemy as DB to other sub modules so they can define 
their database models even the database instance is not created yet.
2. provide a function called ``createDatabase`` to attach database to 
sqlalchemy, so it can get access to these databases (which would be sqlite
or mysql database).

Author: BriFuture

Modified: 2020/05/13 20:56
解决了 mysql 中 lost connection 的错误
@refrence 
    1. https://towardsdatascience.com/use-flask-and-sqlalchemy-not-flask-sqlalchemy-5a64fafe22a4
    2. https://github.com/pallets/flask-sqlalchemy/
    3. https://docs.sqlalchemy.org/en/13/orm/contextual.html

Modified: 2020/06/19 replace property session with scoped_session_maker
Modified: 2021/10/21
    解决 context 中的 内存泄漏问题

Usage
```
from . import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % SQLITE_DATABASE_LOC
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy( app )
```
"""

__version__ = '0.2.1'
import math

def paginate(self, page=None, per_page=None, to_dict=True):
    """
    分页函数
    :param self:
    :param page:
    :param per_page:
    :return:
    """
    if page is None:
        page = 1

    if per_page is None:
        per_page = 20

    items = self.limit(per_page).offset((page - 1) * per_page).all()

    if not items and page != 1:
        return {'total': 0, 'page': page, 'error': 'no such items'}
        
    if page == 1 and len(items) < per_page:
        total = len(items)
    else:
        total = self.order_by(None).count()
    
    if to_dict:
        ditems = [item.to_dict() for item in items]
    else:
        ditems = items

    return {
        'page': page, 
        'per_page': per_page, 
        'total': total, 
        'items': ditems
    }
    # return Pagination(self, page, per_page, total, items)

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base, as_declarative, declared_attr
# Model = declarative_base()

@as_declarative()
class _Model(object):
    # @declared_attr
    # def query():
    #     return 
    query = None
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    # id = Column(Integer, primary_key=True)
sqlalchemy.Model = _Model
orm.Query.paginate = paginate

# Database Proxy
import time
import logging, sys
import threading
from bffacilities import createLogger

class Database(object):
    """Recommond Usage: 
    ```
    db = Database(dbname)
    with db as sess:
        sess.add(Record())
        sess.commit()
    ```
    But it is compatible with flask_sqlalchemy, 
    but scopefunc must be set when construct database instance, @see create_engine
    """
    Column = sqlalchemy.Column
    Integer = sqlalchemy.Integer
    SmallInteger = sqlalchemy.SmallInteger
    BigInteger = sqlalchemy.BigInteger
    Boolean = sqlalchemy.Boolean
    Enum = sqlalchemy.Enum
    Float = sqlalchemy.Float
    Interval = sqlalchemy.Interval
    Numeric = sqlalchemy.Numeric
    PickleType = sqlalchemy.PickleType
    String = sqlalchemy.String
    Text = sqlalchemy.Text
    DateTime = sqlalchemy.DateTime
    Date = sqlalchemy.Date
    Time = sqlalchemy.Time
    Unicode = sqlalchemy.Unicode
    UnicodeText = sqlalchemy.UnicodeText
    LargeBinary = sqlalchemy.LargeBinary
    # MatchType = sqlalchemy.MatchType
    # SchemaType = sqlalchemy.SchemaType
    ARRAY = sqlalchemy.ARRAY
    BIGINT = sqlalchemy.BIGINT
    BINARY = sqlalchemy.BINARY
    BLOB = sqlalchemy.BLOB
    relationship = sqlalchemy.orm.relationship
    ForeignKey = sqlalchemy.ForeignKey
    Table = sqlalchemy.Table

    Model = _Model
    _SessionFactory = orm.sessionmaker()

    def __init__(self, dbname, logger=None, delay_engine_create=False, **kwargs):
        """db used to replace flask_sqlalchemy to provide more convinient ways to manage app
        @pool_recycle 默认的刷新时间为 10 分钟
        @Session use Session instead session property to get scoped session, 
            but scopefunc must be set before Session could be used
        @see createEngine

        kwargs scopefunc
        """
        if logger is None:
            logger = createLogger("db", savefile=False, stream=True, level=logging.DEBUG)
        self.logger = logger

        if 'pool_recycle' not in kwargs:
            kwargs['pool_recycle'] = 600
        # kwargs['pool_recycle'] = 5 # TEST
        self._refresh = kwargs['pool_recycle'] - 1
        
        self.create_all = _Model.metadata.create_all
        self.drop_all = _Model.metadata.drop_all
        if not delay_engine_create:
            self.create_engine(dbname, **kwargs)

    def create_engine(self, dbname, **kwargs):
        """::kwargs:: 
        scopefunc
            if flask is used, `scopefunc=_app_ctx_stack.__ident_func__` could be passed in kwargs
        """
        scopefunc = kwargs.pop('scopefunc', None)
        engine = sqlalchemy.create_engine(dbname, **kwargs)
        _Model.metadata.bind = engine
        
        Database._SessionFactory.configure(bind=engine)
        # _Session is the scoped session maker
        self.Session = orm.scoped_session(Database._SessionFactory, scopefunc=scopefunc)
        # used for compatibility with flask_sqlalchemy, session is scoped
        # self.session = self.Session
        _Model.query = self.Session.query_property()

        self.engine = engine
        self._sessions = {}
        self._ctxsessions = {}
        self._sessionIds = []
        # self.singleSession = dbname.startswith("sqlite")
        self.singleSession = False

    @property
    def session(self):
        """compat with flask_sqlalchemy, not recommand 

        Try use 
        ```
        with database as  sess:
            sess.insert...
        ```
        or
        ```
        sess = database.Session()
        
        ...

        sess.close()
        ```

        """
        id = 0 if self.singleSession else threading.get_ident()
        # self.logger.debug(f"GetSession: {id} {len(self._sessions)}")
        self.check_sessions()

        sess = self._sessions.get(id, None)
        if sess is not None:
            return sess
        count = len(self._sessions)
        if count >= 1000:
            sids = self._sessionIds[:count]
            self._sessionIds = self._sessionIds[count:]
            for sid in sids:
                sess = self._sessions.pop(sid)
                sess.close()
            # return
        sess = self.Session()
        self.logger.debug(f"Create Session For: {id}")
        self._sessions[id] = sess
        self._sessionIds.append(id)
        return sess

    def check_sessions(self):
        # remove useless sessions

        removeneed = []
        for kid, sess in self._sessions.items():
            if not self.valid_session(sess):
                removeneed.append((kid, sess))
                self.logger.debug(f"Found Invalid Session: {kid} {sess}")

        for rn in removeneed:
            self._sessions.pop(rn[0])
            try:
                rn[1].close()
            except: 
                self.logger.debug(f"Close Session Error: {rn[0]} {rn[1]}")

    @staticmethod
    def valid_session(sess):
        try:
            # Try to get the underlying session connection, If you can get it, it's up
            connection = sess.connection()
            # connection.close()
        except:
            return False
        return True

    def close(self):
        self.Session.remove()

    def __enter__(self):
        id = threading.get_ident()
        sess = self._ctxsessions.get(id, None)
        if sess is not None:
            return sess
        ses = self.Session()
        self._ctxsessions[id] = sess
        return ses

    def __exit__(self, exc_type, exc_val, exc_tb):
        id = threading.get_ident()
        a = self._ctxsessions.pop(id)
        if a is not None:
            try:
                a.close()
            except:
                pass
        if exc_type:
            self.logger.warning(f"Type: {exc_type}, value: {exc_val}, {exc_tb}")


# Database Proxy
def createDatabase(dbname, **kwargs):
    """create instance of sqlalchemy Database
    """
    db = Database(dbname, **kwargs)
    logger = logging.getLogger('db')
    logger.warning("[DB] Use Class Database directly")
    return db