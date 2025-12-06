from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/calculations",
    tags=["Calculations"],
)


def _user_column():
    """Return the user FK column (user_id or owner_id) if present."""
    if hasattr(models.Calculation, "user_id"):
        return models.Calculation.user_id
    if hasattr(models.Calculation, "owner_id"):
        return models.Calculation.owner_id
    return None


def _set_user_fk_kwargs(current_user: models.User) -> dict:
    """Build kwargs for user fk that match the model (user_id / owner_id)."""
    kwargs: dict = {}
    if hasattr(models.Calculation, "user_id"):
        kwargs["user_id"] = current_user.id
    elif hasattr(models.Calculation, "owner_id"):
        kwargs["owner_id"] = current_user.id
    return kwargs


# ----- Browse: GET /calculations -----
@router.get("/", response_model=List[schemas.CalculationOut])
def browse_calculations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    user_col = _user_column()
    query = db.query(models.Calculation)

    if user_col is not None:
        query = query.filter(user_col == current_user.id)

    return query.all()


# ----- Read: GET /calculations/{id} -----
@router.get("/{calculation_id}", response_model=schemas.CalculationOut)
def read_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    user_col = _user_column()
    query = db.query(models.Calculation).filter(models.Calculation.id == calculation_id)

    if user_col is not None:
        query = query.filter(user_col == current_user.id)

    calculation = query.first()

    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    return calculation


# ----- Add: POST /calculations -----
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CalculationOut)
def add_calculation(
    payload: schemas.CalculationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    op = payload.operation
    a = payload.a
    b = payload.b

    # compute result on backend
    if op == "add":
        result = a + b
    elif op == "subtract":
        result = a - b
    elif op == "multiply":
        result = a * b
    elif op == "divide":
        if b == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot divide by zero",
            )
        result = a / b
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported operation: {op}",
        )

    # Build kwargs dynamically to match your model
    calc_kwargs = {
        "result": result,
    }

    # Your table has a NOT NULL 'type' column – use it to store the operation name
    if hasattr(models.Calculation, "type"):
        calc_kwargs["type"] = op

    # numeric columns: a/b or operand1/operand2
    if hasattr(models.Calculation, "a") and hasattr(models.Calculation, "b"):
        calc_kwargs["a"] = a
        calc_kwargs["b"] = b
    else:
        calc_kwargs["operand1"] = a
        calc_kwargs["operand2"] = b

    # add user fk if the model has it
    calc_kwargs.update(_set_user_fk_kwargs(current_user))

    calculation = models.Calculation(**calc_kwargs)
    db.add(calculation)
    db.commit()
    db.refresh(calculation)
    return calculation


# ----- Edit: PUT /calculations/{id} -----
@router.put("/{calculation_id}", response_model=schemas.CalculationOut)
def edit_calculation(
    calculation_id: int,
    payload: schemas.CalculationUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    user_col = _user_column()
    query = db.query(models.Calculation).filter(models.Calculation.id == calculation_id)

    if user_col is not None:
        query = query.filter(user_col == current_user.id)

    calculation = query.first()

    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        # remap operation -> type if your model only has 'type'
        if key == "operation":
            if hasattr(calculation, "operation"):
                setattr(calculation, "operation", value)
            elif hasattr(calculation, "type"):
                setattr(calculation, "type", value)
            continue

        # allow updating either a/b or operand1/operand2 depending on model
        if key in ("a", "b") and not hasattr(calculation, key):
            mapped = "operand1" if key == "a" else "operand2"
            if hasattr(calculation, mapped):
                setattr(calculation, mapped, value)
            continue

        setattr(calculation, key, value)

    db.commit()
    db.refresh(calculation)
    return calculation


# ----- Delete: DELETE /calculations/{id} -----
@router.delete("/{calculation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    user_col = _user_column()
    query = db.query(models.Calculation).filter(models.Calculation.id == calculation_id)

    if user_col is not None:
        query = query.filter(user_col == current_user.id)

    calculation = query.first()

    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    db.delete(calculation)
    db.commit()
    return None
