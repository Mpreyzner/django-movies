import requests
import json

url = 'http://127.0.0.1:8000/api/'
timeout = 1


def test_top():
    response = requests.get(url + 'top/', {'from': '01-01-1970', 'to': '07-05-2019'}, timeout=1)
    try:
        response.raise_for_status()
    except Exception as exc:
        print(str(exc))
    assert response.status_code == requests.codes.ok
    assert len(response.json()) > 0


def test_get_movies():
    response = requests.get(url + 'movies/', timeout=1)
    try:
        response.raise_for_status()
    except Exception as exc:
        print(str(exc))
    assert response.status_code == requests.codes.ok
    assert len(response.json()) > 0


def test_post_movie():
    response = requests.post(url + 'movies/', {'title': 'Serenity'}, timeout=1)
    try:
        print(response.content)
        response.raise_for_status()
    except Exception as exc:
        print(str(exc))
    assert response.status_code in (requests.codes.created, requests.codes.ok)
    assert len(response.json()) > 0


def test_get_comments():
    response = requests.get(url + 'comments/', timeout=1)
    try:
        response.raise_for_status()
    except Exception as exc:
        print(str(exc))
    assert response.status_code == requests.codes.ok
    assert len(response.json()) > 0


def test_add_commeents():
    headers = {'content-type': 'application/json'}
    response = requests.post(url + 'comments/',
                             json.dumps({"movie": '013350f4-8758-453c-a956-04284dd18173', "content": 'was not impressed'}),
                             timeout=1, headers=headers)
    try:
        response.raise_for_status()
    except Exception as exc:
        print(str(exc))
    assert response.status_code == requests.codes.created
    assert len(response.json()) > 0
