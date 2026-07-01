from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from scalar_fastapi import get_scalar_api_reference

app = FastAPI(
    title="Shipment Tracking API",
    description="A simple API for retrieving shipment information.",
    version="1.0.0",
)


shipments = {
    12701: {"weight": 0.6, "content": "glassware", "status": "placed"},
    12702: {"weight": 2.3, "content": "books", "status": "shipped"},
    12703: {"weight": 1.1, "content": "electronics", "status": "delivered"},
    12704: {"weight": 3.5, "content": "furniture", "status": "in transit"},
    12705: {"weight": 0.9, "content": "clothing", "status": "returned"},
    12706: {"weight": 4.0, "content": "appliances", "status": "processing"},
    12707: {"weight": 1.8, "content": "toys", "status": "placed"},
}


class Shipment(BaseModel):
    id: int
    weight: float
    content: str
    status: str


@app.get(
    "/shipments",
    response_model=Shipment,
    tags=["Shipments"],
    summary="Retrieve a shipment",
    description="Returns shipment information for the given shipment ID.",
)
def get_shipment(shipment_id: int):
    """
    Example:
        GET /shipments?shipment_id=12704
    """

    shipment = shipments.get(shipment_id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment {shipment_id} was not found.",
        )

    return {
        "id": shipment_id,
        **shipment,
    }


@app.get("/scalar", include_in_schema=False)
def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
