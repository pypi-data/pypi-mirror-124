from flask.testing import FlaskClient

from energytt_platform.api import Application, HttpResponse

from .endpoints import EndpointReturnsGeneric


class TestHeaders:

    def test__endpoint_returns_redirect(
            self,
            app: Application,
            client: FlaskClient,
    ):
        """
        TODO

        :param app:
        :param client:
        :return:
        """

        # -- Arrange ---------------------------------------------------------

        response = HttpResponse(
            status=200,
            headers={
                'Header1': 'Value1',
                'Header2': 'Value2',
            }
        )

        app.add_endpoint(
            method='GET',
            path='/something',
            endpoint=EndpointReturnsGeneric(response),
        )

        # -- Act -------------------------------------------------------------

        r = client.get('/something')

        # -- Assert ----------------------------------------------------------

        assert r.status_code == 200
        assert r.headers['Header1'] == 'Value1'
        assert r.headers['Header2'] == 'Value2'
