# soad_project_2020
# SOAD PROJECT 2020

Visit our dev docs at [devSite](https://hrs2203.github.io/soad_project_2020/)

### BACKEND AND API

TODO LIST : 
- [x] To place an order
- [x] To place a bulk of order, maybe from different business (ideally for small business and single customer)
- [x] Confirm Order devlivery.
- [x] Generate New Apparal.
- [x] Upload an order (maybe an image with description and cost)
- [x] Generate an apparel.
- [x] Get your business detail
- [x] Get your user account detail
- [x] Stats of you sales compared to others.
- [ ] API to add money to account. Transactions happen on our platform



### IMAGE_GEN
Black box for me.

### OTHER

1. Install postgresql on Ubuntu 18.04 ( 
[Link to WebSite](https://www.postgresql.org/download/linux/ubuntu/) )

```
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install postgresql
```

2. Setup Psql on local machine ( For Ubuntu Only ) (
[Link to Website](https://djangocentral.com/using-postgresql-with-django/) )

3. DbConfig

```
CREATE USER soad_user WITH ENCRYPTED PASSWORD 'soad_password_123';
```

4. In case when db is causing problems

- drop db 
- create new database 
- grant privilages to your local user account

```psql
drop database soad
create database soad
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
```
