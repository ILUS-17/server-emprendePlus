from sqlmodel import Session, select
from db.models import Business, Product, Sale, SaleProduct, Finance, Budget, User
from faker import Faker
from datetime import datetime
import random
from uuid import uuid4

fake = Faker()

PRODUCTS = 10
SALES = 15
FINANCES = 10
BUDGETS = 2

def create_random_date():
    return fake.date_time_between(start_date='-1y', end_date='now')

def generate_dummy_data_for_user(user: User, session: Session) -> str:
    user_id = user.id
    business = session.exec(select(Business).where(Business.owner_id == user_id)).first()

    # Si ya tiene negocio, cancelar
    #if not business:
    #   raise ValueError("El usuario ya tiene un negocio generado.")

    business = Business(
        name=fake.company(),
        description=fake.catch_phrase(),
        owner_id=user.id,
        tagline=fake.bs(),
        currency="USD",
        timezone="America/Panama",
        language="es",
        invoice_prefix="INV",
        invoice_counter=random.randint(100, 999)
    )
    session.add(business)
    session.commit()

    # Crear productos
    products = []
    for _ in range(PRODUCTS):
        cost = round(random.uniform(5, 100), 2)
        sale_price = round(cost * random.uniform(1.2, 1.8), 2)
        product = Product(
            sku=fake.unique.lexify("PRD????"),
            business_id=business.id,
            name=fake.word().capitalize(),
            type=random.choice(["physical", "digital"]),
            cost=cost,
            sale_price=sale_price,
            stock=random.randint(10, 100),
            description=fake.sentence(),
            discount=round(random.uniform(0, 0.3), 2),
            min_stock_alert=random.randint(5, 20),
            supplier=fake.company(),
            status=random.choice(["active", "inactive"]),
            color=random.choice(["red", "blue", "green", "black"]),
            width=round(random.uniform(1.0, 10.0), 2),
            height=round(random.uniform(1.0, 10.0), 2),
            depth=round(random.uniform(1.0, 10.0), 2),
            weight=round(random.uniform(0.1, 5.0), 2),
            tax_rate=random.choice([0.07, 0.10]),
            created_at=str(datetime.now()),
            updated_at=str(datetime.now()),
            rating=round(random.uniform(1.0, 5.0), 1),
            image_path=fake.image_url()
        )
        session.add(product)
        products.append(product)
    session.commit()

    # Crear ventas
    for _ in range(SALES):
        sale_date = create_random_date()
        selected_products = random.sample(products, k=random.randint(1, 4))
        total = 0.0
        sale = Sale(
            business_id=business.id,
            sale_date=sale_date,
            total=0.0
        )
        session.add(sale)
        session.commit()

        for prod in selected_products:
            qty = random.randint(1, 5)
            subtotal = round(prod.sale_price * qty, 2)
            sale_product = SaleProduct(
                sale_id=sale.id,
                product_id=prod.sku,
                quantity=qty,
                subtotal=subtotal,
                discount=0.0,
                product_name=prod.product_name,
                sale_price=prod.sale_price
            )
            total += subtotal
            session.add(sale_product)

        sale.total = round(total, 2)
        session.add(sale)
        session.commit()

    # Crear finanzas
    for _ in range(FINANCES):
        finance = Finance(
            business_id=business.id,
            date=create_random_date(),
            type=random.choice(["income", "expense"]),
            category=random.choice(["marketing", "logistics", "admin", "operations"]),
            subcategory=fake.word(),
            amount=round(random.uniform(50, 1500), 2),
            description=fake.sentence()
        )
        session.add(finance)

    # Crear presupuestos
    for _ in range(BUDGETS):
        budget = Budget(
            business_id=business.id,
            category=random.choice(["marketing", "logistics", "admin"]),
            subcategory=random.choice([None, fake.word()]),
            amount=round(random.uniform(1000, 5000), 2)
        )
        session.add(budget)

    session.commit()

    return str(business.id)
