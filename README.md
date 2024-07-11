To run my application you need to install poetry.
This is a tutorial https://python-poetry.org/docs/#installation
If you want to develop this project you need PostgresSQL to run migrations. Create two databases
with QuizAppDB name and TestQuizAppDB, in both set owner to superadmin

When you made changes in models run:
- alembic revision --autogenerate -m "<name_for_migrations>"
- alembic upgrade head

To run my application using docker run this commands:
- docker-compose build
- docker-compose up

To test my application use:
- pytest -v app/tests 