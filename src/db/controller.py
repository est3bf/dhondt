import atexit
import logging
from contextlib import contextmanager
from urllib.parse import quote_plus as urlquote

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database


logger = logging.getLogger(__name__)

DB_CONNECTION_TIMEOUT = 5


class DBNotConnectedError(Exception):
    pass


class DBSessionAlreadyOpen(Exception):
    pass


class DBNoOpenSession(Exception):
    pass


class DB:
    """
    DB class utilities

    default server: 127.0.0.1:5432

    @param url: IP:PORT
    @param database: database name
    @param user: database user to login
    @param passw: database passw to login
    """

    engine = None
    Base = declarative_base()
    session_factory = None
    __session = None

    @classmethod
    def init(cls, url, database, user=None, passw=None, debug=False):
        cls.url = url
        cls.database = database
        cls.user = user
        passw = passw
        cls.passw = urlquote(passw)
        logger.info(
            "Init DB. Server: %s, database : %s, usuario: %s",
            cls.url,
            cls.database,
            cls.user,
        )
        try:
            cls.engine = create_engine(
                "postgresql://{user}:{passw}@{url}/{database}".format(
                    user=cls.user, passw=cls.passw, url=cls.url, database=cls.database
                ),
                connect_args={
                    "connect_timeout": DB_CONNECTION_TIMEOUT,
                },
                echo=debug,
            )

            if not database_exists(cls.engine.url):
                logger.info("No hay DATABASE, LA CREA")
                create_database(cls.engine.url)

            cls.session_factory = sessionmaker(
                bind=cls.engine,
                expire_on_commit=False,
            )
            cls.Base.metadata.create_all(cls.engine)
            logger.info("Supuestamente creo todo!!!!!")

        except Exception as e:
            logger.error("DB init error!!: %s", e)
            raise e

        atexit.register(cls.cleanup)

    @classmethod
    def get_open_session(cls):
        return cls.__session

    @classmethod
    def get_session(cls):
        if cls.session_factory is None:
            raise DBNotConnectedError()
        return cls.session_factory()

    @classmethod
    def cleanup(cls):
        # ONLY TO BE CALLED AT EXIT
        if cls.engine:
            cls.engine.dispose()


@contextmanager
def get_db_session():
    session = DB.get_session()
    try:
        yield session
    finally:
        session.close()
