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

## Esecuzione Locale
Per l'esecuzione in locale è necessario avere python installto, poi eseguire i seguenti comandi:
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
`db.sqlite3` è il file del database SQLite.
Il database è già stato prepolato eseguendo 
```bash
python manage.py seed_demo
```
Lo stesso script è stato eseguito sul databse del deploy.

## Account Demo

| Ruolo     | Username     | Password     |
|-----------|--------------|--------------|
| Superuser | admin_demo   | admin12345   |
| Manager   | manager_demo | manager12345 |
| Customer  | user_demo    | user12345    |

## Deployment
https://mysite-7bsf.onrender.com

## API Endpoints
| Metodo   | URL                      | Auth  | Ruolo           | Body della richiesta              | Risposta               | Descrizione                                |
|----------|--------------------------|-------|-----------------|-----------------------------------|------------------------|--------------------------------------------|
| POST     | /api/auth/register/      | No    | any             | `{"username","email","password"}` | 201 user               | Registrazione utente                       |
| POST     | /api/token/              | No    | any             | `{"username","password"}`         | 200 `{access,refresh}` | Login                                      |
| POST     | /api/token/refresh/      | No    | any             | `{"refresh"}`                     | 200 `{access}`         | Refresh del token                          |
| GET      | /api/auth/me/            | Yes   | any             | –                                 | user object            | Visualizzazione account                    |
| GET      | /api/products/           | No    | any             | –                                 | list                   | Catalogo del prodotti                      |
| POST     | /api/products/           | Yes   | manager         | product fields                    | 201                    | Crea un prodotto                           |
| PATCH    | /api/products/{id}/      | Yes   | manager         | partial fields                    | 200                    | Aggiorna i dati di un prodotto             |
| DELETE   | /api/products/{id}/      | Yes   | manager         | –                                 | 204                    | Cancella un prodotto                       |
| GET/POST | /api/categories/         | mixed | manager (write) | category fields                   | –                      | Gestione categiore                         |
| GET      | /api/cart/               | Yes   | customer        | –                                 | items                  | Visualizzazione del carrello               |
| POST     | /api/cart/               | Yes   | customer        | `{"product_id","quantity"}`       | 201                    | Aggiungi al carrello                       |
| POST     | /api/checkout/           | Yes   | customer        | –                                 | 201 order              | Passaggio da carrello ad ordine (Checkout) |
| GET      | /api/orders/             | Yes   | any             | –                                 | list                   | Gestione degli ordini                      |
| PATCH    | /api/orders/{id}/status/ | Yes   | manager         | `{"status"}`                      | 200                    | Aggiornamento stato ordine                 |

## Test con HTTPie
Per testare le funzionalità, eseguire il seguente workflow con HTTPie (deve essesere installato localmente).
- Se si vuole testare in locale: 
```bash 
export BASE=":8000""
```
- Se si vuole testare dul deploy: 
```bash 
export BASE="https://mysite-7bsf.onrender.com"
```

