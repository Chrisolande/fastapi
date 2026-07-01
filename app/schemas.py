from enum import Enum

from pydantic import BaseModel, Field


class ShipmentStatus(str, Enum):
    placed = "placed"
    shipped = "shipped"
    in_transit = "in transit"
    delivered = "delivered"
    returned = "returned"


class ShipmentCreate(BaseModel):
    content: str = Field(..., min_length=1)
    weight: float = Field(..., gt=0)
    status: ShipmentStatus = ShipmentStatus.placed


class ShipmentUpdate(BaseModel):
    content: str | None = Field(default=None, min_length=1)
    weight: float | None = Field(default=None, gt=0)
    status: ShipmentStatus | None = None


class ShipmentResponse(BaseModel):
    id: int
    content: str
    weight: float
    status: ShipmentStatus
