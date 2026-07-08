# E-Commerce Track Assignment
## Python Execution
To start the app run:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```
## Project Structure

| Types                   |                                                              |
|-------------------------|--------------------------------------------------------------|
| Apps                    | Products, Orders, Accounts                                   |
| Relations               | Product→Category (FK), Order→OrderItem (FK), Order→User (FK) |
| Custom User             | User with a `role` field                                     |
| Rolse with Permissions  | customer, store_manager                                      |
| Classe-Baseed Endpoints |                                                              |
| Input Validation        | DRF serializers                                              |
| CRUD on main resource   | Product                                                      |
| JWT auth                | djangorestframework-simplejwt                                |
| Demo Data               |                                                              |
| Testing Woflow          |                                                              |

The project was started with the base PyCharm settings.