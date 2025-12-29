from sqlalchemy.orm import Session
from app.models import User, Product, Order, OrderItem
from app.schemas import UserCreate, ProductCreate, ProductUpdate, OrderCreate, OrderUpdate
from app.core.security import get_password_hash, verify_password
from datetime import timedelta
from app.core.security import create_access_token
from app.core.config import settings

# User Services
def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def authenticate_user(db: Session, username: str, password: str) -> User:
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token_for_user(user: User) -> str:
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    return create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

# Product Services
def create_product(db: Session, product: ProductCreate, seller_id: int) -> Product:
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        seller_id=seller_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product_by_id(db: Session, product_id: int) -> Product:
    return db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()

def get_all_products(db: Session, skip: int = 0, limit: int = 100) -> list[Product]:
    return db.query(Product).filter(Product.is_active == True).offset(skip).limit(limit).all()

def get_user_products(db: Session, seller_id: int, skip: int = 0, limit: int = 100) -> list[Product]:
    return db.query(Product).filter(
        Product.seller_id == seller_id,
        Product.is_active == True
    ).offset(skip).limit(limit).all()

def update_product(db: Session, product_id: int, product_update: ProductUpdate, seller_id: int) -> Product:
    db_product = db.query(Product).filter(
        Product.id == product_id,
        Product.seller_id == seller_id
    ).first()
    
    if not db_product:
        return None
    
    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int, seller_id: int) -> bool:
    db_product = db.query(Product).filter(
        Product.id == product_id,
        Product.seller_id == seller_id
    ).first()
    
    if not db_product:
        return False
    
    db_product.is_active = False
    db.add(db_product)
    db.commit()
    return True

# Order Services
def create_order(db: Session, order: OrderCreate, buyer_id: int) -> Order:
    total_amount = 0
    items_list = []
    
    # Validate products and calculate total
    for item in order.items:
        product = get_product_by_id(db, item.product_id)
        if not product:
            return None
        
        if product.stock < item.quantity:
            return None
        
        total_amount += product.price * item.quantity
        items_list.append({
            "product": product,
            "quantity": item.quantity,
            "price": product.price
        })
    
    # Create order
    db_order = Order(
        buyer_id=buyer_id,
        total_amount=total_amount
    )
    db.add(db_order)
    db.flush()
    
    # Create order items and update stock
    for item_data in items_list:
        order_item = OrderItem(
            order_id=db_order.id,
            product_id=item_data["product"].id,
            quantity=item_data["quantity"],
            price=item_data["price"]
        )
        db.add(order_item)
        
        # Update product stock
        item_data["product"].stock -= item_data["quantity"]
        db.add(item_data["product"])
    
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order_by_id(db: Session, order_id: int) -> Order:
    return db.query(Order).filter(Order.id == order_id).first()

def get_user_orders(db: Session, buyer_id: int, skip: int = 0, limit: int = 100) -> list[Order]:
    return db.query(Order).filter(
        Order.buyer_id == buyer_id
    ).offset(skip).limit(limit).all()

def update_order_status(db: Session, order_id: int, status_update: OrderUpdate, buyer_id: int) -> Order:
    db_order = db.query(Order).filter(
        Order.id == order_id,
        Order.buyer_id == buyer_id
    ).first()
    
    if not db_order:
        return None
    
    db_order.status = status_update.status
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def cancel_order(db: Session, order_id: int, buyer_id: int) -> bool:
    db_order = db.query(Order).filter(
        Order.id == order_id,
        Order.buyer_id == buyer_id,
        Order.status == "pending"
    ).first()
    
    if not db_order:
        return False
    
    # Restore stock
    for item in db_order.items:
        item.product.stock += item.quantity
        db.add(item.product)
    
    db_order.status = "cancelled"
    db.add(db_order)
    db.commit()
    return True
