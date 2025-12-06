from typing import Optional
from pydantic import BaseModel, EmailStr, constr, model_validator


# -------- User Schemas --------

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: constr(min_length=1, max_length=128)


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


# -------- Calculation Schemas --------

class CalculationBase(BaseModel):
    a: float
    b: float
    type: str  # "Add", "Sub", "Multiply", "Divide"
    user_id: Optional[int] = None


class CalculationCreate(CalculationBase):
    # Pydantic v2-style validator that runs after the model is built
    @model_validator(mode="after")
    def check_divide_by_zero(self):
        # make type check case-insensitive so "divide" and "Divide" both work
        if self.type and self.type.lower() == "divide" and self.b == 0:
            # This ValueError is wrapped into a ValidationError by Pydantic
            raise ValueError("Cannot divide by zero")
        return self


class CalculationRead(CalculationBase):
    id: int
    result: Optional[float] = None

    class Config:
        from_attributes = True
# --- Auth-related user schemas ---
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserLogin(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        # Pydantic v1 style for SQLAlchemy models
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
from typing import Optional
from datetime import datetime

# ----- Calculation Schemas for BREAD -----

class CalculationCreate(CalculationBase):
    """
    Data required to create a calculation.
    Front-end will send operation, operand1, operand2.
    Result is computed in the backend.
    """
    pass


class CalculationUpdate(BaseModel):
    """
    Fields that can be edited. All optional so we can send partial updates.
    """
    operation: Optional[str] = None
    operand1: Optional[float] = None
    operand2: Optional[float] = None


class CalculationOut(CalculationBase):
    """
    What we return to the client when browsing/reading calculations.
    """
    id: int
    result: float
    created_at: Optional[datetime] = None
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

# ----- FINAL Calculation Schemas (BREAD) -----

class CalculationBase(BaseModel):
    operation: str
    a: float
    b: float

    # Pydantic v2: allow reading from ORM models
    model_config = ConfigDict(from_attributes=True)


class CalculationCreate(CalculationBase):
    """
    Data required to create a calculation.
    """
    pass


class CalculationUpdate(BaseModel):
    """
    Fields that can be edited. All optional for partial updates.
    """
    operation: Optional[str] = None
    a: Optional[float] = None
    b: Optional[float] = None


class CalculationOut(CalculationBase):
    """
    What we return to the client when browsing/reading calculations.
    """
    id: int
    result: float
    created_at: Optional[datetime] = None
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

# ----- FINAL Calculation Schemas -----

class CalculationCreate(BaseModel):
    operation: str
    a: float
    b: float


class CalculationUpdate(BaseModel):
    operation: Optional[str] = None
    a: Optional[float] = None
    b: Optional[float] = None


class CalculationOut(BaseModel):
    id: int

    # we prefer operation, but operator is also allowed on the model
    operation: Optional[str] = None
    operator: Optional[str] = None

    # numeric fields – we accept both naming styles from ORM
    a: Optional[float] = None
    b: Optional[float] = None
    operand1: Optional[float] = None
    operand2: Optional[float] = None

    result: Optional[float] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

# ===== Final calculation schemas (override older ones) =====

class CalculationCreate(BaseModel):
    operation: str
    a: float
    b: float


class CalculationUpdate(BaseModel):
    operation: Optional[str] = None
    a: Optional[float] = None
    b: Optional[float] = None


class CalculationOut(BaseModel):
    id: int

    # DB column that stores the operation name
    type: Optional[str] = None

    # alternative names, if present on the model
    operation: Optional[str] = None
    operator: Optional[str] = None

    # numeric fields – support both naming styles
    a: Optional[float] = None
    b: Optional[float] = None
    operand1: Optional[float] = None
    operand2: Optional[float] = None

    result: Optional[float] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, model_validator

# ===== FINAL calculation schemas (override earlier ones) =====

class CalculationCreate(BaseModel):
    a: float
    b: float
    # tests send "type", UI sends "operation"; support both
    type: str
    operation: Optional[str] = None

    @model_validator(mode="after")
    def _normalize_and_validate(self):
        # Pick whichever is set and normalize to lowercase
        op_raw = self.operation or self.type
        if not op_raw:
            raise ValueError("operation is required")

        op = op_raw.lower()
        self.operation = op
        self.type = op

        if op not in {"add", "subtract", "multiply", "divide"}:
            raise ValueError("Invalid operation")

        # For divide, enforce b != 0 so tests see "Cannot divide by zero"
        if op == "divide" and self.b == 0:
            raise ValueError("Cannot divide by zero")

        return self


class CalculationUpdate(BaseModel):
    a: Optional[float] = None
    b: Optional[float] = None
    type: Optional[str] = None
    operation: Optional[str] = None

    @model_validator(mode="after")
    def _normalize_op(self):
        if self.operation or self.type:
            op_raw = self.operation or self.type
            op = op_raw.lower()
            self.operation = op
            self.type = op
        return self


class CalculationOut(BaseModel):
    id: int

    # operation name – DB column is "type" but we also expose "operation"
    type: Optional[str] = None
    operation: Optional[str] = None
    operator: Optional[str] = None

    # operands; support both naming styles
    a: Optional[float] = None
    b: Optional[float] = None
    operand1: Optional[float] = None
    operand2: Optional[float] = None

    result: Optional[float] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
class OperationCount(BaseModel):
    operator: str
    count: int


class UsageSummary(BaseModel):
    total_calculations: int
    per_operation: list[OperationCount]
    last_calculation_at: datetime | None
