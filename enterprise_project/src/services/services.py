from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.core.security import create_token, hash_password, verify_password
from src.models.models import Order, OrderItem, Product, User


class ServiceError(Exception):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.message, self.status = message, status


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, email: str, password: str, role: str = "customer") -> User:
        if self.db.query(User).filter_by(email=email).first():
            raise ServiceError("Email already registered", 409)
        user = User(email=email, password_hash=hash_password(password), role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def login(self, email: str, password: str) -> str:
        user = self.db.query(User).filter_by(email=email.lower()).first()
        if not user or not verify_password(password, user.password_hash):
            raise ServiceError("Invalid credentials", 401)
        return create_token(user.id, user.role)


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def list(self, skip: int = 0, limit: int = 100):
        return self.db.query(Product).order_by(Product.id).offset(skip).limit(limit).all()

    def create(self, data, user_id: int) -> Product:
        p = Product(**data.model_dump(), created_by=user_id)
        self.db.add(p)
        self.db.commit()
        self.db.refresh(p)
        return p


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data, user_id: int) -> Order:
        total, lines = 0.0, []
        for it in data.items:
            p = self.db.get(Product, it.product_id)
            if not p:
                raise ServiceError(f"Product {it.product_id} not found", 404)
            if p.stock < it.quantity:
                raise ServiceError(f"Insufficient stock for '{p.name}'", 409)
            p.stock -= it.quantity
            total += p.price * it.quantity
            lines.append(OrderItem(product_id=p.id, quantity=it.quantity, unit_price=p.price))
        order = Order(user_id=user_id, total=round(total, 2),
                      created_at=datetime.now(timezone.utc).isoformat(), items=lines)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def for_user(self, user_id: int):
        return self.db.query(Order).filter_by(user_id=user_id).all()
