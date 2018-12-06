def test_new_user(new_user):
    print(new_user.id)
    assert new_user.first_name == 'Laurene'
    assert new_user.middle_name == 'Ngoya'
    assert new_user.last_name == 'Mutundu'
    assert new_user.username == 'Lmutu'
    assert new_user.email == 'lmutu@mail.com'
    assert new_user.password_hash != 'Lmutu'
    assert not new_user.is_anonymous
    

def test_new_business(new_business):
    assert new_business.name == 'testBus'
    assert new_business.category == 'testCat'
    assert new_business.location == 'testLoc'
    assert new_business.desctiption == 'testDesc'


def test_new_review(new_review):
    assert new_review.business_id == 999
    assert new_review.user_id == 999
    assert new_review.post == 'post'