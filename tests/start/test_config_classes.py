from stats.start.config import (
    BaseConfig, DevelopmentConfig, ProductionConfig, TestingConfig
)
from stats.start.environment import APP_NAME, FAVICON, HTML_LANG, TITLE


def test_base_config():
    conf = BaseConfig()

    assert conf.APP_NAME == APP_NAME
    assert conf.BCRYPT_LOG_ROUNDS == 13
    assert conf.DEBUG is False
    assert conf.FAVICON == FAVICON
    assert conf.HTML_LANG == HTML_LANG
    assert conf.SECRET_KEY and isinstance(conf.SECRET_KEY, (str, bytes))
    assert conf.TESTING is False
    assert conf.TITLE == TITLE
    assert conf.WTF_CSRF_ENABLED is True
    assert conf.WTF_CSRF_SSL_STRICT is True


def test_devel_config():
    conf = DevelopmentConfig()

    assert conf.DEBUG is True
    assert conf.SQLALCHEMY_DATABASE_URI.startswith('sqlite:////')
    assert conf.TESTING is False
    assert conf.TITLE == TITLE


def test_test_config():
    conf = TestingConfig()

    assert conf.BCRYPT_LOG_ROUNDS == 5
    assert conf.DEBUG is False
    assert conf.SQLALCHEMY_DATABASE_URI == 'sqlite://'
    assert conf.TESTING is True
    assert conf.TITLE == TITLE
    assert conf.WTF_CSRF_ENABLED is False


def test_prod_config():
    conf = ProductionConfig()

    assert conf.DEBUG is False
    assert conf.SQLALCHEMY_DATABASE_URI == 'sqlite://'
    assert conf.TESTING is False
    assert conf.TITLE == TITLE
