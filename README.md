Invoice System

Welcome to the Invoice System repository! This project is a Django-based application for managing invoices with features such as invoice generation, QR code integration, and multilingual support.

## Features

- **Invoice Management**: Create, view, and download invoices.
- **QR Code Integration**: Each invoice includes a scannable QR code for easy verification and access.
- **Multilingual Support**: Change the application language as per user preference.
- **Dark Theme**: A modern dark theme for a better user experience.
- **Customer Management**: Add, edit, and manage customer information seamlessly.

## Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS
- **Database**: SQLite

## Installation

Follow the steps below to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Fouda-Emmanuel/Invoice.git
   cd Invoice
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the Server**:
   ```bash
   python manage.py runserver
   ```
   Access the application at `http://127.0.0.1:8000/`.

## Usage

1. Navigate to the application homepage.
2. Add a new customer by filling in the required details.
3. Generate an invoice for a customer.
4. Download the invoice with the embedded QR code.
5. Switch between available languages as needed.

## Project Structure

The project is structured as follows:

```
Invoice/
├── invoiceproj/       # Project configuration files
├── invoice_app/       # Main application files
├── templates/         # HTML templates
├── static/            # Static files (CSS, JS, images)
├── locale/            # Language files for multilingual support
├── db.sqlite3         # SQLite database
├── manage.py          # Django management script
└── requirements.txt   # Project dependencies
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push to your fork:
   ```bash
   git push origin feature-name
   ```
4. Open a pull request with a detailed description of your changes.
5. 

## Contact

For any inquiries or support, please reach out to:
- **Author**: Fouda Emmanuel
- **Email**: leoemmanuelson46@gmail.com

Thank you for using the Invoice System!

