from uuid import uuid4

import pytest
from datetime import datetime
from itertools import product
from flask.testing import FlaskClient
from typing import Dict, Iterable, Any

from energytt_platform.api.testing import CookieTester
from energytt_platform.api import Application, HttpResponse, Cookie

from .endpoints import EndpointReturnsGeneric


def get_cookie_combinations() -> Iterable[Dict[str, Any]]:
    """
    TODO
    """

    combinations = product(
        (None, True, False),     # http_only
        (None, True, False),     # secure
        (None, True, False),     # same_site
        (None, 'domain.com'),    # domain
        (None, '/path'),         # path
        (None, datetime.now()),  # expires
    )

    for http_only, secure, same_site, domain, path, expires in combinations:
        yield {
            'name': str(uuid4()),
            'value': str(uuid4()),
            'http_only': http_only,
            'secure': secure,
            'same_site': same_site,
            'domain': domain,
            'path': path,
            'expires': expires,
        }


class TestCookies:

    @pytest.mark.parametrize('cookie_kwargs', get_cookie_combinations())
    def test__set_one_cookie__should_set_cookie_correctly(
            self,
            cookie_kwargs: Dict[str, Any],
            app: Application,
            client: FlaskClient,
    ):
        """
        TODO
        """

        # -- Arrange ---------------------------------------------------------

        response = HttpResponse(
            status=200,
            cookies=(Cookie(**cookie_kwargs),),
        )

        app.add_endpoint(
            method='GET',
            path='/something',
            endpoint=EndpointReturnsGeneric(response),
        )

        # -- Act -------------------------------------------------------------

        r = client.get('/something')

        # -- Assert ----------------------------------------------------------

        CookieTester(r.headers) \
            .assert_has_cookies(cookie_kwargs['name']) \
            .assert_cookie(**cookie_kwargs)

    def test__set_multiple_cookies__should_set_all_cookies_correctly(
            self,
            app: Application,
            client: FlaskClient,
    ):
        """
        TODO
        """

        # -- Arrange ---------------------------------------------------------

        response = HttpResponse(
            status=200,
            cookies=(
                Cookie(name='Cookie1', value='Value1', same_site=True),
                Cookie(name='Cookie2', value='Value2'),
                Cookie(name='Cookie3', value='Value3'),
            ),
        )

        app.add_endpoint(
            method='GET',
            path='/something',
            endpoint=EndpointReturnsGeneric(response),
        )

        # -- Act -------------------------------------------------------------

        r = client.get('/something')

        # -- Assert ----------------------------------------------------------

        CookieTester(r.headers) \
            .assert_has_cookies('Cookie1', 'Cookie2', 'Cookie3') \
            .assert_cookie(name='Cookie1', value='Value1', same_site=True) \
            .assert_cookie(name='Cookie2', value='Value2') \
            .assert_cookie(name='Cookie3', value='Value3')
