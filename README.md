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

## Struttura
### Struttura dei file
```
ElaboratoEcommerce/
├── manage.py
├── build.sh                        Build script per Render
├── render.yaml                     File necessario per il deploy su Render
├── requirements.txt
├── README.md
├── db.sqlite3                     
├── .gitignore
├── templates/                  
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
├── products/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── views.py
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
└── orders/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── tests.py
    ├── views.py
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py             
    └── management/
        ├── __init__.py
        └── commands/
            ├── __init__.py
            └── seed_demo.py                seeding script
```

Il progetto contiene le seguenti applicazioni:
- `accounts`
- `products`
- `orders`

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

I modelli usati nel database, distribuiti tra le tre applicazioni, sono:
- **User:** presente in `accounts/models.py`, che estende la classe AbstractUser di Django (aggiungendo il campo `role`)
- **Category e Products:** presenti in `products/models.py`, descrivono il catalogo dei prodotti.
- **Cart e CartItem:** presenti in `orders/models.py`, rappresentano il carrello.
- **Order e OrderItem:** presenti in `orders/models.py`, rappresentano gli ordini.
## Account Demo

| Ruolo     | Username     | Password     |
|-----------|--------------|--------------|
| Superuser | admin_demo   | admin12345   |
| Manager   | manager_demo | manager12345 |
| Customer  | user_demo    | user12345    |
| Customer  | user2_demo   | user12345    |

## Deployment
Il depoly è stato eseguito su Render:
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

## Esempi di risposta
**Registrazione (POST /api/auth/register/)**
```json
// Richiesta
{"username": "nuovo_utente", "email": "test@test.com", "password": "password123"}

// Risposta 201
{"id": 5, "username": "nuovo_utente", "email": "test@test.com", "role": "customer"}
```

**Errore di validazione (POST /api/products/, prezzo negativo)**
```json
// Risposta 400
{"price": ["Price must be positive."]}
```

**Checkout (POST /api/checkout/)**
```json
// Risposta 201
{"order_id": 4, "total": "39.98"}
```

**Cronologia ordini (GET /api/orders/)**
```json
// Risposta 200
[
  {
    "id": 4,
    "status": "pending",
    "total": "39.98",
    "created_at": "2026-07-10T10:00:00Z",
    "items": [
      {"id": 1, "product": {"id": 1, "name": "Wireless Mouse", "price": "19.99", ...}, "quantity": 2, "price": "19.99"}
    ]
  }
]
```



## Test con HTTPie
È possibile testare le API con HTTPie, scaricandolo da https://httpie.io/ oppure attraverso il package manager del sistema operativo.

Per testare le funzionalità, eseguire il seguente workflow:
- Se si vuole testare in locale: 
  ```bash 
  export BASE=":8000""
  ```
- Se si vuole testare sul deploy: 
  ```bash 
  export BASE="https://mysite-7bsf.onrender.com"
  ```

1. **Accesso Pubblico:**
    ```bash
    http GET $BASE/api/products/
    http GET $BASE/api/categories/
    ```
2. **Login come cliente:**
    ```bash
   http POST $BASE/api/token/ username=user_demo password=user12345
   ```
   Dal JSON restituito, copiare il token `"access"` fornito, e per praticità impostarlo come variabile, poi eseguire l'autentizazione:
    ```bash
   export TOKEN="<copriare il token qui>"
   http GET $BASE/api/auth/me/ "Authorization:Bearer $TOKEN"
   ```
   (Accesso e visualizzazione del profilo)
3. **Gestione Carrello:**
    ```bash
   http GET $BASE/api/cart/ "Authorization:Bearer $TOKEN"
   http POST $BASE/api/cart/ "Authorization:Bearer $TOKEN" product_id=2 quantity=1
    ```
   (Visualizzazione e aggiunta di un prodotto)


4. **Checkout:**
    ```bash
   http POST $BASE/api/checkout/ "Authorization:Bearer $TOKEN"
    http GET $BASE/api/orders/ "Authorization:Bearer $TOKEN"
    ```
   (Passaggio da carrello ad ordine, visualizzazione degli ordini)


5. **Azioni Vietate:**
    ```bash
    http POST $BASE/api/products/ "Authorization:Bearer $TOKEN" name=Hack slug=hack price=1 stock=1 category=electronics
    ```
   (Cliente che prova ad aggiungere un prodotto al catalogo, viene restuito 403 Forbidden)
   
    ```bash
   http POST $BASE/api/token/ username=user2_demo password=user12345
    export TOKEN2="<paste access token>"
    http GET $BASE/api/cart/ "Authorization:Bearer $TOKEN2"     # expect empty
    http GET $BASE/api/orders/ "Authorization:Bearer $TOKEN2"
    ```
   (Un cliente prova ad accedere al carello e agli ordini di un altro cliente)


6. **Login Manager:**
    ```bash
    http POST $BASE/api/token/ username=manager_demo password=manager12345
    ```
   Come per il login come customer di prima, dal JSON di risposta si copia il token `"access"` e si imposta una variabile
   ```bash
   export MTOKEN=""
   ```
   (Accesso come manager)
   ```bash
   http PATCH $BASE/api/orders/1/status/ "Authorization:Bearer $MTOKEN" status=paid
    ```
   (Il manager può aggiornare gli stati di un ordine)


7. **Operazioni CRUD sui prodotti:**
    ```bash
    http GET $BASE/api/products/ "Authorization:Bearer $MTOKEN"
    http POST $BASE/api/products/ "Authorization:Bearer $MTOKEN" name=TV slug=tv price=1 stock=1 category=electronics
    http PATCH $BASE/api/products/1/ "Authorization:Bearer $MTOKEN" name=TV slug=tv price=2 stock=2 category=electronics
    http DELETE $BASE/api/products/1/ "Authorization:Bearer $MTOKEN"
    ```
   (in ordine: visualizzazione, creazione, aggioramento e rimozione dei prodotti)


8. **Aggiornamento dello stato di un ordine:**
    ```bash
    http PATCH $BASE/api/orders/1/status/
   ```
   (Aggiornamento dello stato dell'ordine, riservato al manager)