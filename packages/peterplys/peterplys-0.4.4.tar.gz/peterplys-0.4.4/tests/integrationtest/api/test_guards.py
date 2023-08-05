from typing import List
from uuid import uuid4

import pytest
from flask.testing import FlaskClient

from energytt_platform.api import (
    Application,
    EndpointGuard,
    TokenGuard,
    ScopedGuard,
)

from .endpoints import EmptyEndpoint


class TestGuards:
    """
    TODO
    """

    @pytest.mark.parametrize('guard', [
        TokenGuard(),
        ScopedGuard('scope1'),
    ])
    def test__provide_no_token__should_return_status_401(
            self,
            guard: EndpointGuard,
            app: Application,
            client: FlaskClient,
    ):
        """
        TODO
        """

        # -- Arrange ---------------------------------------------------------

        app.add_endpoint(
            method='POST',
            path='/something',
            endpoint=EmptyEndpoint(),
            guards=[guard],
        )

        # -- Act -------------------------------------------------------------

        r = client.post('/something')

        # -- Assert ----------------------------------------------------------

        assert r.status_code == 401

    @pytest.mark.parametrize('guard', [
        TokenGuard(),
        ScopedGuard('scope1'),
    ])
    def test__provide_invalid_token__should_return_status_401(
            self,
            guard: EndpointGuard,
            app: Application,
            client: FlaskClient,
    ):
        """
        TODO
        """

        # -- Arrange ---------------------------------------------------------

        app.add_endpoint(
            method='POST',
            path='/something',
            endpoint=EmptyEndpoint(),
            guards=[guard],
        )

        # -- Act -------------------------------------------------------------

        r = client.post(
            path='/something',
            headers={'Authorization': f'Bearer: NOT-A-VALID-TOKEN'},
        )

        # -- Assert ----------------------------------------------------------

        assert r.status_code == 401

    @pytest.mark.parametrize('guard', [
        TokenGuard(),
        ScopedGuard('scope1'),
    ])
    def test__provide_valid_token__should_return_status_200(
            self,
            guard: EndpointGuard,
            app: Application,
            client: FlaskClient,
            valid_token_encoded: str,
    ):
        """
        TODO
        """

        # -- Arrange ---------------------------------------------------------

        app.add_endpoint(
            method='POST',
            path='/something',
            endpoint=EmptyEndpoint(),
            guards=[guard],
        )

        # -- Act -------------------------------------------------------------

        r = client.post(
            path='/something',
            headers={'Authorization': f'Bearer: {valid_token_encoded}'},
        )

        # -- Assert ----------------------------------------------------------

        assert r.status_code == 200

    def test__token_missing_required_scope__should_return_status_401(
            self,
            app: Application,
            client: FlaskClient,
            valid_token_encoded: str,
    ):
        """
        TODO
        """

        # -- Arrange ---------------------------------------------------------

        required_scope = str(uuid4())  # Something random

        app.add_endpoint(
            method='POST',
            path='/something',
            endpoint=EmptyEndpoint(),
            guards=[ScopedGuard(required_scope)],
        )

        # -- Act -------------------------------------------------------------

        r = client.post(
            path='/something',
            headers={'Authorization': f'Bearer: {valid_token_encoded}'},
        )

        # -- Assert ----------------------------------------------------------

        assert r.status_code == 401

    @pytest.mark.parametrize('guards', [
        [ScopedGuard('scope1')],
        [ScopedGuard('scope2')],
        [ScopedGuard('scope1', 'scope2')],
        [TokenGuard(), ScopedGuard('scope1')],
        [TokenGuard(), ScopedGuard('scope1', 'scope2')],
        [TokenGuard(), ScopedGuard('scope1'), ScopedGuard('scope2')],
    ])
    def test__token_has_required_scope__should_return_status_200(
            self,
            guards: List[EndpointGuard],
            app: Application,
            client: FlaskClient,
            valid_token_encoded: str,
    ):
        """
        TODO
        """

        # -- Arrange ---------------------------------------------------------

        app.add_endpoint(
            method='POST',
            path='/something',
            endpoint=EmptyEndpoint(),
            guards=guards,
        )

        # -- Act -------------------------------------------------------------

        r = client.post(
            path='/something',
            headers={'Authorization': f'Bearer: {valid_token_encoded}'},
        )

        # -- Assert ----------------------------------------------------------

        assert r.status_code == 200
