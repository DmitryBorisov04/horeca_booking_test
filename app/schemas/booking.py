import re
from datetime import date, time, timedelta
from typing import Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict


class BookingBase(BaseModel):
    name: str = Field(..., min_length=2, examples=["Иван Иванов"])
    phone: str = Field(..., examples=["+79991234567"])
    booking_date: date = Field(..., examples=["2026-08-30"])
    booking_time: time = Field(..., examples=["18:00:00"])
    guests: int = Field(..., ge=1, le=12, examples=[4])

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not re.fullmatch(r"^[A-Za-zА-Яа-яЁё\s\-]+$", value):
            raise ValueError(
                "Имя может содержать только буквы, пробелы и дефис.")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        digits = re.sub(r'\D', '', value)
        if len(digits) == 11 and digits[0] in ('7', '8'):
            return f"+7{digits[1:]}"
        raise ValueError("Введите корректный номер: +7 или 8, 10 цифр")

    @field_validator("booking_date")
    @classmethod
    def validate_booking_date(cls, value: date) -> date:
        today = date.today()
        if value < today:
            raise ValueError("Дата не может быть в прошлом.")
        if value > today + timedelta(days=90):
            raise ValueError("Бронь возможна не более чем на 90 дней вперед.")
        return value

    @field_validator("booking_time")
    @classmethod
    def validate_booking_time(cls, value: time) -> time:
        if value.minute != 0 or value.second != 0 or value.hour < 12 or value.hour > 22:
            raise ValueError(
                "Только слоты: 12:00, 13:00 ... 22:00 (шаг 1 час).")
        return time(hour=value.hour, minute=0, second=0)


class BookingCreate(BookingBase):
    pass


class BookingOut(BookingBase):
    id: int
    status: Literal["active", "cancelled"]

    model_config = ConfigDict(from_attributes=True)
