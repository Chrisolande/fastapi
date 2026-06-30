import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scalar_fastapi import get_scalar_api_reference


class ShipmentResponse(BaseModel):
    id: int
    tracking_number: str
    customer: str
    weight: float
    status: str
    origin: str
    destination: str


class ShipmentRepository:
    def get_by_id(self, shipment_id: int):

        shipments = {
            1: {
                "id": 1,
                "tracking_number": "KE123456",
                "customer": "Chris",
                "weight": 1.2,
                "status": "In Transit",
                "origin": "Nairobi",
                "destination": "Mombasa",
            },
            2: {
                "id": 2,
                "tracking_number": "KE987654",
                "customer": "Alice",
                "weight": 4.8,
                "status": "Delivered",
                "origin": "Kisumu",
                "destination": "Nakuru",
            },
        }

        return shipments.get(shipment_id)


class ShipmentService:
    def __init__(self):
        self.repository = ShipmentRepository()

    def get_shipment(self, shipment_id: int):

        shipment = self.repository.get_by_id(shipment_id)

        if shipment is None:
            raise ValueError("Shipment not found")

        return shipment


app = FastAPI(title="Shipment Tracking API")

service = ShipmentService()


@app.get("/shipments/{shipment_id}", response_model=ShipmentResponse)
def get_shipment(shipment_id: int):

    try:
        return service.get_shipment(shipment_id)

    except ValueError:
        raise HTTPException(status_code=404, detail="Shipment not found")


@app.get("/scalar", include_in_schema=False)
def scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Shipment API")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
