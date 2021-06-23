----Chuong trinh quan ly dao tao----

    Link git: https://github.com/LongPhanPip/qldt

    Clone from git:
        git clone https://github.com/LongPhanPip/qldt qldt

    Push to git:
        git remote add origin https://github.com/LongPhanPip/qldt
        git push -u origin master

    Prequisite:
        Python: 3.8
        Mysql: 8.0
        Docker

    Run:
        Init:
            docker-compose up -d

        Debug log:
            docker-compose logs

        Execute command:
            docker-compose exec backend [command]

        ReBuild:
            docker-compose --build

        #warning: Don't update or delete data directly to database
        Access database:
            docker-compose exec db mysql -u root -p qldt_db
            Enter password: 123456

## Setup without docker
1. Install pipenv
2. pipenv install
3. Delete all the migrations folders
4. Delete .db folder
5. Open mysql with username and password
6. Go to settings.py in config folder, find DATABASES dict, type your username and password, port(default is 3306), host(use localhost), name(database name)
7. Go to mysql(mysql -u <USERNAME> -p) create database with the name above(CREATE DATABASE <DATABASE_NAME>)
8. pipenv shell
9. python manage.py makemigrations accounts persons students teachers school
10. python manage.py migrate
11. python manage.py createsuperuser
12. python manage.py runserver

