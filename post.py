from enum import Enum
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field
from scalar_fastapi import get_scalar_api_reference


class ShipmentStatus(str, Enum):
    """Valid shipment statuses."""
    PLACED = "placed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    RETURNED = "returned"


class ShipmentCreate(BaseModel):
    """Request schema for creating a shipment."""
    content: str = Field(..., min_length=1, max_length=100)
    weight: float = Field(..., gt=0, le=25, description="Weight in kilograms (max 25 kg)")


class ShipmentResponse(ShipmentCreate):
    """Response schema for a shipment."""
    id: int = Field(..., description="Unique shipment identifier")
    status: ShipmentStatus = Field(default=ShipmentStatus.PLACED)

    model_config = {"json_schema_extra": {"example": {
        "id": 12701,
        "content": "glassware",
        "weight": 0.6,
        "status": "placed"
    }}}


class ShipmentStore:
    """In-memory shipment storage with ID management."""

    def __init__(self):
        self._shipments: dict[int, dict] = {
            12701: {"content": "glassware", "weight": 0.6, "status": ShipmentStatus.PLACED},
            12702: {"content": "books", "weight": 2.3, "status": ShipmentStatus.SHIPPED},
            12703: {"content": "electronics", "weight": 1.1, "status": ShipmentStatus.DELIVERED},
            12704: {"content": "furniture", "weight": 3.5, "status": ShipmentStatus.IN_TRANSIT},
            12705: {"content": "clothing", "weight": 0.9, "status": ShipmentStatus.RETURNED},
            12706: {"content": "appliances", "weight": 4.0, "status": ShipmentStatus.PROCESSING},
            12707: {"content": "toys", "weight": 1.8, "status": ShipmentStatus.PLACED},
        }
        self._next_id = max(self._shipments.keys()) + 1

    def get(self, shipment_id: int) -> dict:
        """Retrieve a shipment by ID."""
        if shipment_id not in self._shipments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shipment {shipment_id} not found"
            )
        return self._shipments[shipment_id]

    def create(self, shipment: ShipmentCreate) -> int:
        """Create a new shipment and return its ID."""
        new_id = self._next_id
        self._next_id += 1
        self._shipments[new_id] = {
            **shipment.model_dump(),
            "status": ShipmentStatus.PLACED
        }
        return new_id

    def list_all(self) -> dict[int, dict]:
        """Retrieve all shipments."""
        return self._shipments


store = ShipmentStore()

app = FastAPI(
    title="Shipment Management API",
    description="Track and manage shipments with real-time status updates",
    version="2.0.0",
)


@app.get(
    "/shipment/{shipment_id}",
    response_model=ShipmentResponse,
    summary="Get shipment details",
    tags=["Shipments"]
)
def get_shipment(
    shipment_id: Annotated[int, Path(..., gt=0, description="Shipment ID")]
) -> ShipmentResponse:
    """Retrieve details for a specific shipment."""
    data = store.get(shipment_id)
    return ShipmentResponse(id=shipment_id, **data)


@app.post(
    "/shipment",
    response_model=ShipmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new shipment",
    tags=["Shipments"]
)
def create_shipment(
    shipment: ShipmentCreate
) -> ShipmentResponse:
    """Create a new shipment. Weight must not exceed 25 kg."""
    new_id = store.create(shipment)
    data = store.get(new_id)
    return ShipmentResponse(id=new_id, **data)


@app.get(
    "/shipments",
    response_model=dict[int, ShipmentResponse],
    summary="List all shipments",
    tags=["Shipments"]
)
def list_shipments() -> dict[int, ShipmentResponse]:
    """Retrieve all shipments."""
    all_shipments = store.list_all()
    return {
        sid: ShipmentResponse(id=sid, **data)
        for sid, data in all_shipments.items()
    }


# API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    """Scalar API documentation."""
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Shipment API Documentation",
    )
