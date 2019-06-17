import pytest
import requests
import tenacity


def test_returns_204_when_stuff_gets_up(docker_services):
    app_port = docker_services.port_for('contaiwaiter', 8080)
    response = _get_app_response(app_port)
    assert response.status_code == 204


@tenacity.retry(stop=tenacity.stop_after_delay(5), wait=tenacity.wait_fixed(0.2))
def _get_app_response(app_port: int) -> requests.Response:
    return requests.get(f'http://localhost:{app_port}')
