def test_app(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Biashara' in response.data


def test_login_logout(test_client, init_database):
    # test login functionality
    with test_client:
        response = test_client.post('/login',
                                    data=dict(username='Lmutu', password='Lmutu'),
                                    follow_redirects=True)
        assert response.status_code == 200
        # assert b"Reviews" in response.data
        # assert b"Lmutu" in response.data
        # assert b"Register Business" in response.data
        # assert b"Choose" in response.data
        # assert b"Log out" in response.data
        # assert b"Log in" not in response.data
        
        # #########test logout functionality
        response = test_client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        # assert b"Biashara is a web app" in response.data
        # assert b"Biashara" in response.data
        # assert b"Log out" not in response.data
        # assert b"Log in" in response.data
        # assert b"Sign up" in response.data