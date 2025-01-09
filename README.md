### Todo App with Django rest framework and JWT Authentication
---
This project is a django rest framework web application that includes a Task and custom user with authentication JWT.

#### Features
---
+ User authentication
    + Custom user model
    + Signup, signin, logout functionality
    + Verify registration with OTP code
+ Task
    + Create, Delete, Detail, Favorite

#### Project Structure
---
```bash
.
├── accounts
│   ├── admin.py                # Accounts admin configuration
│   ├── apps.py                 # Accounts apps configuration
│   ├── authentication.py       # Check User exists
│   ├── managers.py
│   ├── models.py               # Accounts models (User, OTPCode)
│   ├── serializers.py          # Accounts serializer
│   ├── tests.py
│   ├── urls.py                 # Accounts URL configuration
│   └── views.py                # Accounts view              
├── core
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── LICENSE
├── manage.py                   # Django's command-line utility
├── README.md
├── requirements.txt            # Python dependencies
└── task
    ├── admin.py                # Task admin configuration
    ├── apps.py                 # Task apps configuration
    ├── models.py               # Task models (Task, Category, Favorite)
    ├── serializers.py          # Task Serializers (TaskSerializer)
    ├── tests.py
    ├── urls.py                 # Task URL configuration
    └── views.py                # Task view
```

#### Setup Instructions

1. Clone the repository:

   ```bash
   git clone git@github.com:cyhssin/todo-app.git
   ```

2. Install dependencies:

   ```bash
   python -m venv .env
   source ./.env/bin/activate
   pip install -r requirements.txt
   ```

3. Apply migrations:

   ```bash
   python manage.py migrate
   ```

4. Run the development server:

   ```bash
   python manage.py runserver
   ```

5. Access the site at `http://127.0.0.1:8000/`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Developed by [cyhssin](https://github.com/cyhssin)