import pytest
from httpx import AsyncClient

@pytest.mark.parametrize("room_id,date_from,date_to,status_code", [
    *[(4, "2030-05-01", "2030-05-15", 200)] * 8,
    # (4, "2030-05-01", "2030-05-15", 409),
    # (4, "2030-05-01", "2030-05-15", 409)
])
async def test_add_and_get_booking(auth_ac: AsyncClient, room_id, date_from, date_to, status_code):
    response = await auth_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code

    # тут не дописал