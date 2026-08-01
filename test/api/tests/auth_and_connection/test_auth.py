import pytest
import requests

from test_utils.data_factories.api_user import APIUserFactory




def test_login_failure(api_client):
    """Test login with invalid credentials"""
    with pytest.raises(Exception) as exc_info:
        api_client.login(username="invalid_user", password="invalid_pass")

    assert not api_client.is_authenticated()
    assert api_client.token is None



def test_register_success(api_client):
    """Test successful user registration and subsequent login"""
    # Create a new random user
    user = APIUserFactory.create()

    # Register new user
    response = api_client.register(user)
    assert response['message'] == 'User created successfully'
    assert not api_client.is_authenticated()

    login_response = api_client.login(user)
    assert 'access_token' in login_response
    assert api_client.is_authenticated()
    assert user.is_authenticated

    # Clean up by deleting the user
    api_client.delete_account()



# def test_register_duplicate_user(api_client):
#     """Test registration with existing username"""
#     user = APIUserFactory.create()
#     # First register a user
#     api_client.register(user)
#     api_client.logout()  # Clear the session
#
#     user.password = APIUserFactory.generate_password()
#
#     # Try to register the same username again
#     with pytest.raises(Exception) as exc_info:
#         api_client.register(user)
#
#     # need to confirm the right exception or some kind of api feedback



@pytest.fixture(autouse=True)
def cleanup_after_test(api_client):
    """Ensure client is logged out after each test"""
    yield
    api_client.logout()