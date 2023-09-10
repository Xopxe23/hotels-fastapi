from fastapi import APIRouter, Depends

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    bookings = await BookingDAO.find_all(user_id=user.id)
    return bookings


@router.get("/{id}")
async def get_booking_by_id(booking_id: int) -> SBooking:
    return await BookingDAO.find_by_id(booking_id)
