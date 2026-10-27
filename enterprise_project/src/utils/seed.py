"""Create an admin user and sample products: python -m src.utils.seed"""
from src.core.database import Base, SessionLocal, engine
from src.models import models  # noqa: F401
from src.models.models import Product
from src.services.services import ServiceError, UserService

Base.metadata.create_all(engine)
db = SessionLocal()
try:
    UserService(db).register("admin@example.com", "ChangeMe123!", role="admin")
except ServiceError:
    pass
if not db.query(Product).count():
    db.add_all([Product(name="Laptop", price=55000, stock=10), Product(name="Headphones", price=2850, stock=50)])
    db.commit()
print("Seeded. Admin: admin@example.com / ChangeMe123!")
