from app.hotels.models import Hotels
from app.hotels.router import router


@router.get("/{hotel_id}/rooms")
def get_rooms(name: str) -> Hotels:
    pass
