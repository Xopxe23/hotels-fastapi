from fastapi import FastAPI, Query, Depends
from typing import Optional
from datetime import date

from pydantic import BaseModel
from app.bookings.router import router as bookings_router

app = FastAPI()
app.include_router(bookings_router)


class SHotel(BaseModel):
    address: str
    name: str
    stars: int


class HotelSearchArgs:
    def __init__(self,
                 location: str,
                 date_from: date,
                 date_to: date,
                 has_spa: Optional[bool] = None,
                 stars: Optional[int] = Query(None, ge=1, le=5)
                 , ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars


@app.get("/hotels")
def get_hotels(
        search_args: HotelSearchArgs = Depends()
) -> list[SHotel]:
    hotels = [
        {
            "address": "Gagarin street 12",
            "name": "Super hotel",
            "stars": 5
        },
    ]

    return hotels


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post("/bookings")
def add_booking(booking: SBooking):
    pass
