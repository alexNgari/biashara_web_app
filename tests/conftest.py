import pytest
from app import app
from app.models import User, Business, Review


################    MODELS  ####################
@pytest.fixture(scope='module')
def new_user():
    user = User(first_name='Laurene', middle_name='Ngoya', last_name='Mutundu', username='Lmutu', email='lmutu@mail.com')
    user.set_password('Lmutu')
    return user

@pytest.fixture(scope='module')
def new_business():
    business = Business(name='testBus', category='testCat', desctiption='testDesc', location='testLoc')
    return business

@pytest.fixture(scope='module')
def new_review():
    review = Review(user_id=999, business_id=999, post='post')
    return review


##############  FUNCTIONAL TESTS    #########################
@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield app_client
    ctx.pop()

