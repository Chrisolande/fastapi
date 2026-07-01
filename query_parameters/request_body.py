from enum import Enum
from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()


class ShipmentStatus(str, Enum):
    PLACED = "placed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    IN_TRANSIT = "in transit"
    RETURNED = "returned"
    PROCESSING = "processing"


class Shipment(BaseModel):
    weight: float = Field(
        ..., description="Weight in kgs", le=25
    content: str
    status: ShipmentStatus = ShipmentStatus.PLACED


class ShipmentResponse(BaseModel):
    id: int


shipments: dict[int, dict[str, any]] = {
    12701: {"weight": 0.6, "content": "glassware", "status": "placed"},
    12702: {"weight": 2.3, "content": "books", "status": "shipped"},
    12703: {"weight": 1.1, "content": "electronics", "status": "delivered"},
    12704: {"weight": 3.5, "content": "furniture", "status": "in transit"},
    12705: {"weight": 0.9, "content": "clothing", "status": "returned"},
    12706: {"weight": 4.0, "content": "appliances", "status": "processing"},
    12707: {"weight": 1.8, "content": "toys", "status": "placed"},
}

@app.get("/shipments/{shipment_id}", response_model=Shipment)
def get_shipment(
    shipment_id: int = Path(..., description="The ID of the shipment to retrieve"),
):
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )
    return shipments[shipment_id]


@app.post(
    "/shipments", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED
)
def submit_shipment(
    shipment_data: Shipment,
    notes: str | None = Query(None, description="Optional query parameter notes"),
):
    if notes:
        print(f"\nQuery Param Notes: {notes}\n")


    new_id = max(shipments.keys()) + 1

    shipments[new_id] = shipment_data.model_dump()

    return ShipmentResponse(id=new_id)



@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
