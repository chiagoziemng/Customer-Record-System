# Customer Record System for Omar and Blasius Sales Agents

## Project Overview
The **Customer Record System** is a web-based application designed to streamline client management for sales agents at Omar and Blasius. The platform supports role-based access control, client record tracking, reporting, and financial management, ensuring seamless collaboration and efficient operations.

---

## Features
1. **Role-Based Access Control**:
   - Roles: SaleAgent, Manager, and SuperAdmin.
   - Access and permissions are determined based on user roles.

2. **Client Management**:
   - Create, view, and manage client records.
   - Searchable client table with AJAX-powered details view.

3. **Dashboards**:
   - Separate dashboards for SuperAdmin, Manager, and SaleAgent.

4. **Reporting Tools**:
   - Export reports in PDF and Excel formats.
   - Scheduled reports using Celery or Django crontab.

5. **Security Enhancements**:
   - Custom URL for SuperAdmin access.
   - Daily backups to Azure or AWS.
   - Session timeout and account suspension for security breaches.

6. **Financial Management**:
   - Track SaleAgent payments and employment duration.

---

## Project Structure
```
customer_record_system/
├── customer_record_system/  # Project settings and configuration
├── sales/                   # Main app for client and user management
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   ├── static/              # CSS, JS, and assets
│   ├── models.py            # Database models
│   ├── views.py             # Application logic
│   ├── urls.py              # Application routes
│   └── admin.py             # Admin panel customization
└── requirements.txt         # Python dependencies
```

---

## Installation

### Prerequisites
- Python 3.9+
- Django 4.x
- Virtual environment (recommended)

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/omar-and-blasius/customer_record_system.git
   cd customer_record_system
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - Navigate to `http://127.0.0.1:8000/` in your browser.

---

## Key Components

### Models
- **SaleAgent**: Tracks sales agent details such as name, location, and bank details.
- **ClientRecord**: Stores client information, including business details, contact info, and deal status.
- **Manager**: Manages departments and oversees sales agents.
- **SuperAdmin**: Oversees the entire system with advanced privileges.
- **SessionLog**: Logs user actions for auditing purposes.

### Views
- **Login**: Custom login page with role-based access.
- **Client Records**: AJAX-powered client table with detailed record view.
- **Dashboards**: Custom dashboards for each user role.

---

## Deployment

### Production Setup
1. **Set up a production server** (e.g., Ubuntu):
   - Install Gunicorn and Nginx.
   - Configure environment variables for secrets and database settings.

2. **Database**:
   - Switch to PostgreSQL for production.
   - Configure database backups on AWS or Azure.

3. **Static Files**:
   - Run `python manage.py collectstatic` to collect static files.
   - Configure Nginx to serve static files.

4. **Launch Application**:
   ```bash
   gunicorn customer_record_system.wsgi:application --bind 0.0.0.0:8000
   ```

---

## Testing

### Unit Testing
- Run tests using Django's test framework:
  ```bash
  python manage.py test
  ```

### System Testing
- Conduct end-to-end testing for each user role.
- Validate permissions and data access restrictions.

---

## Contribution
We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact
For inquiries or support, please contact:
- **Omar and Blasius Support**: support@omarandblasius.com

---

Happy coding!

