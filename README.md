### MYSQL Ansible Dynamic Inventory

#### Installation

```
git clone https://github.com/tormath1/mysql-dynamic-inventory.git
cd mysql-dynamic-inventory
virtualenv venv
source venv
pip install -r requirements.txt
```

#### Usage

```
ansible -m ping ./inventory.py all
```

#### Configuration

| variable              | description                 | default   |
|-----------------------|-----------------------------|-----------|
| MYSQL_USERNAME        | MySQL username              | username  |
| MYSQL_PASSWORD        | MySQL password              | password  |
| MYSQL_SSL_SKIP_VERIFY | Disable SSL CA verification | None      |
| MYSQL_DATABASE        | MySQL database              | database  |
| MYSQL_PORT            | MySQL port                  | 3306      |
| MYSQL_HOST            | MySQL host                  | localhost |


