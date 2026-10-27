from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import decode_token
from src.models.models import User
from src.models.schemas import Login, OrderCreate, ProductCreate, UserCreate
from src.services.services import OrderService, ProductService, UserService

router = APIRouter()
bearer = HTTPBearer()


def current_user(cred: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> User:
    payload = decode_token(cred.credentials)
    user = db.get(User, int(payload["sub"])) if payload else None
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    return user


def require_admin(user: User = Depends(current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin role required")
    return user


def _p(p):
    return {"id": p.id, "name": p.name, "price": p.price, "stock": p.stock}


def _o(o):
    return {"id": o.id, "total": o.total, "created_at": o.created_at,
            "items": [{"product_id": i.product_id, "quantity": i.quantity, "unit_price": i.unit_price}
                      for i in o.items]}


@router.post("/auth/register", status_code=201, tags=["Auth"])
def register(body: UserCreate, db: Session = Depends(get_db)):
    u = UserService(db).register(body.email, body.password)
    return {"id": u.id, "email": u.email, "role": u.role}


@router.post("/auth/login", tags=["Auth"])
def login(body: Login, db: Session = Depends(get_db)):
    return {"access_token": UserService(db).login(body.email, body.password), "token_type": "bearer"}


@router.get("/products", tags=["Products"])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return [_p(p) for p in ProductService(db).list(skip, min(limit, 500))]


@router.post("/products", status_code=201, tags=["Products"])
def create_product(body: ProductCreate, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    return _p(ProductService(db).create(body, user.id))


@router.post("/orders", status_code=201, tags=["Orders"])
def create_order(body: OrderCreate, db: Session = Depends(get_db), user: User = Depends(current_user)):
    return _o(OrderService(db).create(body, user.id))


@router.get("/orders", tags=["Orders"])
def my_orders(db: Session = Depends(get_db), user: User = Depends(current_user)):
    return [_o(o) for o in OrderService(db).for_user(user.id)]
