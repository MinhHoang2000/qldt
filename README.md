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


        To make new migrations:
            1. delete all migraitons files in qldt
            2. docker-compose exec backend python manage.py makemigrations account school students teachers persons
            3. drop database qldt_db
            4. create database qldt_db
            5. use qldt_db;
            6. docker-compose exec backend python manage.py migrate

        Stop:
            docker-commpose down



