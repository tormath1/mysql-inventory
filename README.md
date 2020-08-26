### MYSQL Ansible Dynamic Inventory

#### Installation

```
git clone https://github.com/tormath1/mysql-inventory.git
cd mysql-dynamic-inventory
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Usage

```
ansible -m ping ./inventory.py all
```

#### Configuration

| variable                                | description                 | default   |
|-----------------------------------------|-----------------------------|-----------|
| ANSIBLE_INVENTORY_MYSQL_USERNAME        | MySQL username              | username  |
| ANSIBLE_INVENTORY_MYSQL_PASSWORD        | MySQL password              | password  |
| ANSIBLE_INVENTORY_MYSQL_SSL_SKIP_VERIFY | Disable SSL CA verification | None      |
| ANSIBLE_INVENTORY_MYSQL_DATABASE        | MySQL database              | database  |
| ANSIBLE_INVENTORY_MYSQL_PORT            | MySQL port                  | 3306      |
| ANSIBLE_INVENTORY_MYSQL_HOST            | MySQL host                  | localhost |

#### Development

Install the `dev` requirements:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

Run the tests:

```
pytest .
```
