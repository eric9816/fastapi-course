import pytest

from app.users.service import UserService


@pytest.mark.parametrize("id,email,exists", [
    (1, "test@test.com", True),
    (2, "artem@example.com", True),
    (3, "eric@mail.com", False)
])
async def test_find_user_by_id(id, email, exists):
    user = await UserService.find_by_id(id)

    if exists:
        assert user
        assert user.id == id
        assert user.email == email
    else:
        assert not user
