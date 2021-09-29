Auction Example application made by Sergei Shurpenkov.

Has following features:
    - Home page with paginated auction items list
    - Ordering feature of items list
    - Search feature of items list
    - Login page
    - Administrator page
    - User page
    - User automatic bidding configuration
    - Create new item page
    - Details of item page with manual o automatic bidding
    - User lanched background threads for automatic bidding

Technologies used in application and required to be installed before running the application:
    - Python v3.7
    - Django v3.2.6
    - Django Rest Framework v3.12.4
    - Angular v12.2.4
    - PostgresSQL

Implantation of application in new host:

    1. Download backend Django code from:
       https://github.com/svsrus/auction-backend-example.git

    2. Download frontend Angular code from:
       https://github.com/svsrus/auction-frontend-example.git

    3. Create a virtual environment if needed.

    4. Download project dependencies with the following command:
       Command: pip install -r requirements.txt
       Example: /scopic-auction-test/pip install -r requirements.txt

    5. Set up postgresql database by running following script in your PostgreSQL:
       /scopic-auction-test/database/01-create-database.sql

    6. Delete all migration files py+pyc in following folders except __init__.py:
       /scopic-auction-test/apps/auction_backend/migrations
       /scopic-auction-test/apps/auction_backend/migrations/__pycache__

    7. Run django migrations:
       /scopic-auction-test/manage.py makemigrations
       /scopic-auction-test/manage.py migrate

    8. Populate data in database using following django command:
       /scopic-auction-test/manage.py loaddata database/02-database-dump.json

    9. Start django development server:
       /scopic-auction-test/manage.py runserver
       (must be started at http://127.0.0.1:8000/)

    10. Start angular development server:
       /scopic-auction-test/apps/auction_frontend/static/auction-angular-frontend/ng serve
       (must be started at http://127.0.0.1:4200/ or http://localhost:4200/)

    11. Use test application by navigating to the following URL in your browser: http://localhost:4200/
