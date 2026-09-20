from app.models.payment import Payment
from sqlalchemy.orm import Session


class PaymentRepository:
    def __init__(self):
        self.model = Payment

    def get(self, db: Session, id: int):
        return db.get(self.model, id)

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def get_by_sale_id(self, db: Session, sale_id: int):
        return db.query(self.model).filter(self.model.sale_id == sale_id).all()

    def create(self, db: Session, data: dict):
        payment = self.model(**data)
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    def update(self, db: Session, db_obj: Payment, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Payment):
        db.delete(db_obj)
        db.commit()


payment_repository = PaymentRepository()