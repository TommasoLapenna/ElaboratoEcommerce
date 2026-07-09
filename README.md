# E-Commerce
- Elaborato Backend Tommaso Lapenna.
- REST API per un E-Commerce
- Django / Django REST Framework

## Descrizione
L'applicazione fornisce una REST API per un e-commerce che permette di visualizzare i prodotti, aggiungerli al carello e effettuare gli ordini. Tutto ciò è monitorato dagli store manager, che hanno accesso a tutte queste informazioni.

## Featuers
- **Customer:** 
  - Navigazioni tra i prodotti e delle categorie
  - Registrazione e login, JWT
  - Gestione del proprio carello, checkout dell'ordine
  - Visualizzazione la propria cronologia degli ordini

- **Manager:**
  - CRUD completo sulle tabelle dei prodotti e delle categorie
  - Visualizzazione ti tutti gli ordini, aggiornamento dello stato di essi

## Python Execution
To start the app, run:
```bash
git clone https://github.com/TommasoLapenna/ElaboratoEcommerce.git
cd ElaboratoEcommerce
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Demo Database
`db.sqlite3` è il file del database SQLite,è prepolato da `python manage.py seed_demo`.

## Account Demo

| Role      | Username     | Password     |
|-----------|--------------|--------------|
| Superuser | admin_demo   | admin12345   |
| Manager   | manager_demo | manager12345 |
| Customer  | user_demo    | user12345    |

## Deployment

## API Endpoints
| Method   | URL                      | Auth  | Role            | Request body                      | Response               | Description                  |
|----------|--------------------------|-------|-----------------|-----------------------------------|------------------------|------------------------------|
| POST     | /api/auth/register/      | No    | any             | `{"username","email","password"}` | 201 user               | Create a customer account    |
| POST     | /api/token/              | No    | any             | `{"username","password"}`         | 200 `{access,refresh}` | Login                        |
| POST     | /api/token/refresh/      | No    | any             | `{"refresh"}`                     | 200 `{access}`         | Refresh token                |
| GET      | /api/auth/me/            | Yes   | any             | –                                 | user object            | Current profile              |
| GET      | /api/products/           | No    | any             | –                                 | list                   | Browse catalogue             |
| POST     | /api/products/           | Yes   | manager         | product fields                    | 201                    | Create product               |
| PATCH    | /api/products/{id}/      | Yes   | manager         | partial fields                    | 200                    | Update product               |
| DELETE   | /api/products/{id}/      | Yes   | manager         | –                                 | 204                    | Delete product               |
| GET/POST | /api/categories/         | mixed | manager (write) | category fields                   | –                      | Manage categories            |
| GET      | /api/cart/               | Yes   | customer        | –                                 | items                  | View own cart                |
| POST     | /api/cart/               | Yes   | customer        | `{"product_id","quantity"}`       | 201                    | Add to cart                  |
| POST     | /api/checkout/           | Yes   | customer        | –                                 | 201 order              | Convert cart to order        |
| GET      | /api/orders/             | Yes   | any             | –                                 | list                   | Own orders (all, if manager) |
| PATCH    | /api/orders/{id}/status/ | Yes   | manager         | `{"status"}`                      | 200                    | Update order status          |

## Test con HTTPie