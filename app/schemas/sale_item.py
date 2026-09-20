from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator


class SaleItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: Decimal
    line_discount: Decimal | None = 0
    line_total: Decimal


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int
    line_discount: Decimal | None = 0

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Quantity must be positive")
        return v


class SaleItemUpdate(BaseModel):
    quantity: int | None = None
    line_discount: Decimal | None = None

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, v: int | None) -> int | None:
        if v is not None and v <= 0:
            raise ValueError("Quantity must be positive")
        return v


class SaleItemRead(SaleItemBase):
    model_config = ConfigDict(from_attributes=True)

    sale_item_id: int
    sale_id: int