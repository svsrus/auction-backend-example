Scopic Auction Test application made by Sergei Shurpenkov.

Application covers 100% of functionality that was specified in the requirements document.

Technologies used in application and required to be installed before running the application:
    - Python v3.7
    - Django v3.2.6
    - Django Rest Framework v3.12.4
    - Angular v12.2.4
    - PostgresSQL



Implantation of application in new host:

    1. Download backend Django code from:
       https://github.com/svsrus/scopic-auction-backend.git

    2. Download frontend Angular code from:
       https://github.com/svsrus/scopic-auction-frontend.git

    1. Create a virtual environment if needed.

    2. Download project dependencies with the following command:
    Command: pip install -r requirements.txt
    Example: /scopic-auction-test/pip install -r requirements.txt

    3. Set up postgresql database by running following script in your PostgreSQL:
    /scopic-auction-test/database/01-create-database.sql

    4. Delete all migration files py+pyc in following folders except __init__.py:
    /scopic-auction-test/apps/auction_backend/migrations
    /scopic-auction-test/apps/auction_backend/migrations/__pycache__

    5. Run django migrations:
    /scopic-auction-test/manage.py makemigrations
    /scopic-auction-test/manage.py migrate

    6. Populate data in database using following django command:
    /scopic-auction-test/manage.py loaddata database/02-database-dump.json

    7. Start django development server:
    /scopic-auction-test/manage.py runserver
    (must be started at http://127.0.0.1:8000/)

    8. Start angular development server:
    /scopic-auction-test/apps/auction_frontend/static/auction-angular-frontend/ng serve
    (must be started at http://127.0.0.1:4200/ or http://localhost:4200/)

    9. Use test application by navigating to the following URL in your browser: http://localhost:4200/