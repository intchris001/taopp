# TAOPP - Online Shopping Platform

TAOPP is a modern e-commerce platform built with Flask, offering a seamless shopping experience for both customers and administrators.

## Features

- **User Management**
  - User registration and authentication
  - Profile management
  - Password recovery

- **Product Management**
  - Category-based product organization
  - Product search functionality
  - Detailed product pages with images
  - Stock management

- **Shopping Experience**
  - Shopping cart functionality
  - Order management
  - Secure checkout process

- **Admin Features**
  - Product management (CRUD operations)
  - Order management
  - User management
  - Stock level monitoring

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: Bootstrap 5, JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Database ORM**: SQLAlchemy

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/taopp.git
   cd taopp
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python clean_db.py
   python app/seed_categories.py
   ```

5. Start the application:
   ```bash
   python run.py
   ```

The application will be available at `http://127.0.0.1:5000/`

## Project Structure

```
taopp/
├── app/
│   ├── models/         # Database models
│   ├── routes/         # Route handlers
│   ├── static/         # Static files (CSS, JS, images)
│   └── templates/      # HTML templates
├── migrations/         # Database migrations
├── .env               # Environment variables
├── config.py          # Configuration settings
├── requirements.txt   # Project dependencies
└── run.py            # Application entry point
```

## Usage

1. **User Registration**
   - Visit the registration page
   - Fill in required information
   - Verify email (if enabled)

2. **Shopping**
   - Browse products by category
   - Add items to cart
   - Proceed to checkout
   - Complete payment

3. **Admin Access**
   - Login with admin credentials
   - Manage products and categories
   - Monitor orders and stock

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Project Link: [https://github.com/yourusername/taopp](https://github.com/yourusername/taopp)

## Acknowledgments

- Bootstrap for the UI components
- Flask and its extensions
- All contributors who have helped with the project 