# Commerce

This folder contains a Django project named `commerce`, which implements an online auction site through a single app called `auctions`. The application allows users to create auction listings, place bids, comment on items, and manage watchlists, with robust authentication features.

## Features

- **User Authentication:** Register, log in, and log out securely.
- **Auction Listings:** Create listings with a title, description, starting bid, optional image, and category.
- **Active Listings:** View all active auctions with details such as title, description, current price, and image.
- **Listing Pages:** See detailed information and bidding history for each auction. Authenticated users can:
  - Add/remove items to/from their personal watchlist.
  - Place bids (must exceed current highest bid or starting bid).
  - Comment on listings.
  - Close their own listings to end the auction and declare a winner.
- **Watchlist:** Authenticated users can view and manage their watchlist.
- **Categories:** Browse listings by category.
- **Django Admin:** Full CRUD for users, auctions, bids, and comments via the Django admin interface.

## Project Structure

```
commerce/
├── auctions/
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── templates/
│   │   └── auctions/
│   │       ├── layout.html
│   │       └── ...
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── commerce/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
└── manage.py
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/KamogeloMahlake/commerce.git
   cd commerce
   ```

2. **Install Dependencies**
   We recommend using a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install django
   ```

3. **Apply Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a Superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` in your browser.

6. **Register an Account**
   - Use the Register link to create a user account.
   - Use the Django Admin at `/admin/` for superuser access.

## Customization

- **Templates:** Modify `auctions/templates/auctions/layout.html` to change the site layout.
- **Models:** Edit `auctions/models.py` to add fields or models. Run `makemigrations` and `migrate` after changes.
