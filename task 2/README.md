# Task 2: E-Commerce API (FastAPI)

A modular FastAPI project implementing a simple shopping API with products, cart, checkout, JWT authentication, response time middleware, and order backup.

## Features
- Modular project structure with routers and modules
  - routers/products.py (admin/public product endpoints)
  - routers/cart.py (cart add/checkout)
  - routers/users.py (auth & registration)
- Product model (SQLModel): id, name, price, stock
- Endpoints
  - POST /admin/products/ (admin only)
  - GET /products/ (public)
  - POST /cart/add/ (authenticated)
  - POST /cart/checkout/ (authenticated)
- JWT authentication for users (password hashing with bcrypt, jose JWT)
- Middleware: measures response time and adds header `X-Process-Time`
- Orders backup persisted to `orders.json` (anchored to Task 2 directory)

## Tech stack
- FastAPI 0.116
- SQLAlchemy 2.x / SQLModel
- Pydantic 2.x
- python-jose, passlib[bcrypt]
- SQLite

## Project structure
- task 2/
  - E-commerce/
    - main.py
    - auth.py, utils.py, database_setup.py
    - models/, crud/, routers/, schemas/
  - e-commerce.db
  - orders.json
  - requirements.txt

## Setup
- Python >= 3.10 recommended
- Install dependencies
  - `pip install -r "task 2/requirements.txt"`

## Running the app
Because the package directory name contains a hyphen, import paths may vary by environment. Two common approaches:

- Use uvicorn with the project root in your PYTHONPATH so the package can be imported:
  - `python -m uvicorn E-commerce.main:app --reload`
- If your environment cannot import packages with hyphens, rename `E-commerce` to a valid module name (e.g., `Ecommerce`) and run:
  - `python -m uvicorn Ecommerce.main:app --reload`

OpenAPI docs at: http://localhost:8000/docs

## Database
- SQLite file: `task 2/e-commerce.db`
- Tables are auto-created on app startup.

## Authentication
- Register: `POST /auth/register` (JSON)
  - Body: { name, username, email, password, age, is_active?, is_admin? }
  - is_active defaults to true if omitted; is_admin defaults to false if omitted.
  - Note: Admin-only endpoints require a user with `is_admin = true`. Creation/escalation of admin users is an operational concern (e.g., update the DB).
- Login: `POST /auth/token` (form data: `username`, `password`)
  - Returns: { access_token, token_type }
  - Use header: `Authorization: Bearer <access_token>` for protected endpoints.

## Endpoints overview
- Public
  - `GET /products/` — list products (pagination via `skip`, `limit`)
  - `GET /products/{product_id}` — get product by ID
- Admin (Bearer token + is_admin)
  - `POST /admin/products/` — create a product
- Cart (Bearer token)
  - `POST /cart/add/` — add item to cart
    - Body: { product_id: int, quantity: int (> 0) }
  - `POST /cart/checkout/` — place order from current cart
    - Saves order to `task 2/orders.json` and clears the cart

## Middleware
- Adds `X-Process-Time` header to every response with the processing time in seconds.

## Orders backup
- All checkouts are appended to `task 2/orders.json` for backup/auditing.

## Notes
- Token URL for Swagger is `/auth/token`.
- Response models support Pydantic v2 ORM serialization.
- Quantity validation ensures positive integers for cart additions.
