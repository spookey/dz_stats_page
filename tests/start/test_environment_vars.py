from observatory.start.environment import APP_NAME, ERROR_CODES, MDL_NAME


def test_appname():
    assert APP_NAME == 'observatory'


def test_modulename():
    assert MDL_NAME == 'observatory'


def test_errorcodes():
    def _check(start, end=None):
        count = 0
        for code in range(start, 1 + (end if end is not None else start)):
            assert code in ERROR_CODES
            count += 1

        return count

    total = sum(
        [
            _check(400, 401),
            _check(403, 404),
            _check(418),
            _check(500, 504),
        ]
    )
    assert len(ERROR_CODES) == total
