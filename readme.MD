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
   git clone https://github.com/chiagoziemng/customer_record_system.git
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

## Conventional commits messages to improve communication

1. Fest: (new feature) 
2. Fix: (bug fix) 
3. Docs: (documentation changes) 
4. Style: (formatting , missing semi-colons, etc) 
5. Refactor: (code changes that neither fixes a bug nor adds a feature) 
6. Test: (adding missing tests or correcting existing tests) 
7. Chore: (changes to the build process or auxiliary tools and libraries)

## With Git Flow, there are at least 5 different types of branches. Let’s describe them first:

1. Main: This branch represents the production-ready state. 
2. Develop: This branch contains the latest delivered changes for the upcoming release. 
3. Feature: Feature branches are where new capabilities for future releases are being developed. 
4. Release: Release branches serve the purpose of preparing a new production release. 
5. Hotfix: Hotfix branches emerge when a critical bug in production requires an immediate fix.

---
## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact
For inquiries or support, please contact:
- **Omar and Blasius Support**: support@omarandblasius.com.ng

---

Happy coding!

