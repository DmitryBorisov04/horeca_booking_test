from datetime import date
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.booking import BookingCreate, BookingOut
from app.services import booking_service

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_in: BookingCreate,
    session: AsyncSession = Depends(get_db)
):
    """Создать новую бронь"""
    return await booking_service.create_booking(session=session, booking_in=booking_in)


@router.get("", response_model=List[BookingOut])
async def get_bookings(
    date: date | None = None,
    session: AsyncSession = Depends(get_db)
):
    """Получить список всех броней (с опциональным фильтром по дате)"""
    return await booking_service.get_bookings(session=session, filter_date=date)


@router.get("/{booking_id}", response_model=BookingOut)
async def get_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Получить информацию о конкретной брони по ID"""
    return await booking_service.get_booking_by_id(session=session, booking_id=booking_id)


@router.delete("/{booking_id}", response_model=BookingOut)
async def cancel_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Отменить бронь (перевести статус в cancelled)"""
    return await booking_service.cancel_booking(session=session, booking_id=booking_id)
