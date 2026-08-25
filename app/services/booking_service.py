from datetime import date
from typing import Sequence
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking
from app.schemas.booking import BookingCreate


async def create_booking(session: AsyncSession, booking_in: BookingCreate) -> Booking:
    """Создание брони с проверкой на занятость столика"""

    stmt = select(Booking).where(
        Booking.booking_date == booking_in.booking_date,
        Booking.booking_time == booking_in.booking_time,
        Booking.status == "active"
    )
    result = await session.execute(stmt)
    existing_booking = result.scalar_one_or_none()

    if existing_booking:
        raise HTTPException(
            status_code=409, detail="Слот на выбранные дату/время уже занят")

    new_booking = Booking(**booking_in.model_dump())
    session.add(new_booking)
    await session.commit()

    return new_booking


async def get_bookings(session: AsyncSession, filter_date: date | None = None) -> Sequence[Booking]:
    """Получение списка броней с опциональным фильтром по дате"""

    stmt = select(Booking)
    if filter_date:
        stmt = stmt.where(Booking.booking_date == filter_date)

    result = await session.execute(stmt)
    return result.scalars().all()


async def get_booking_by_id(session: AsyncSession, booking_id: int) -> Booking:
    """Получение одной брони по id"""

    booking = await session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


async def cancel_booking(session: AsyncSession, booking_id: int) -> Booking:
    """Отмена брони (Soft Delete)"""

    booking = await session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.status = "cancelled"
    await session.commit()
    return booking
