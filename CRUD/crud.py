from fastapi import Depends, FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from app.schemas import ShipmentCreate, ShipmentResponse, ShipmentUpdate
from database.database import Database, get_db

app = FastAPI(title="Modern Shipment Management API")


# CREATE
@app.post(
    "/shipment3s",
    response_model=ShipmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_shipment(payload: ShipmentCreate, db: Database = Depends(get_db)):
    shipment_id = db.create(payload)
    return db.get(shipment_id)


# READ ALL
@app.get("/shipments", response_model=list[ShipmentResponse])
def get_all_shipments(db: Database = Depends(get_db)):
    return db.get_all()


def valid_shipment(shipment_id: int, db: Database = Depends(get_db)):
    shipment = db.get(shipment_id)
    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment


# READ SINGLE
@app.get("/shipments/{shipment_id}", response_model=ShipmentResponse)
def get_shipment(shipment: dict = Depends(valid_shipment)):
    return shipment


# PUT (full replace)
@app.put("/shipments/{shipment_id}", response_model=ShipmentResponse)
def replace_shipment(
    payload: ShipmentCreate,
    shipment: dict = Depends(valid_shipment),
    db: Database = Depends(get_db),
):
    return db.replace(shipment["id"], payload)


# PATCH (partial update)
@app.patch("/shipments/{shipment_id}", response_model=ShipmentResponse)
def modify_shipment(
    payload: ShipmentUpdate,
    shipment: dict = Depends(valid_shipment),
    db: Database = Depends(get_db),
):
    return db.update(shipment["id"], payload)


# DELETE
@app.delete("/shipments/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_shipment(
    shipment: dict = Depends(valid_shipment),
    db: Database = Depends(get_db),
):
    db.delete(shipment["id"])


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Modern CRUD Architecture Docs",
    )
