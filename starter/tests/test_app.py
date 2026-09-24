import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_renders_main_page(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data
    assert b'index.html' not in response.data


def test_new_game_returns_puzzle_data(client):
    response = client.get('/new?clues=35')

    assert response.status_code == 200
    payload = response.get_json()
    assert 'puzzle' in payload
    assert len(payload['puzzle']) == 9
    assert all(len(row) == 9 for row in payload['puzzle'])


def test_new_game_tracks_selected_difficulty(client):
    response = client.get('/new?difficulty=hard')

    assert response.status_code == 200
    with client.session_transaction() as session:
        assert session['difficulty'] == 'hard'


def test_check_solution_requires_active_game(client):
    response = client.post('/check', json={'board': [[0 for _ in range(9)] for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json()['error'] == 'No game in progress'


def test_check_solution_detects_incorrect_positions(client):
    client.get('/new?clues=35')
    board = [[0 for _ in range(9)] for _ in range(9)]
    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    payload = response.get_json()
    assert 'incorrect' in payload
    assert isinstance(payload['incorrect'], list)


def test_hint_returns_one_correct_value_and_tracks_usage(client):
    client.get('/new?clues=35')
    response = client.post('/hint')

    assert response.status_code == 200
    payload = response.get_json()
    assert 'row' in payload
    assert 'col' in payload
    assert 'value' in payload
    assert payload['value'] in range(1, 10)
    assert 'hints_used' in payload
    assert payload['hints_used'] >= 1
