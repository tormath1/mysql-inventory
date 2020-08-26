#!/usr/bin/env python

import os
import json

import mysql.connector
from mysql.connector import errorcode

host = os.getenv("ANSIBLE_INVENTORY_MYQSL_HOST", "localhost")
port = int(os.getenv("ANSIBLE_INVENTORY_MYSQL_PORT", 3306))
username = os.getenv("ANSIBLE_INVENTORY_MYSQL_USERNAME", "username")
password = os.getenv("ANSIBLE_INVENTORY_MYSQL_PASSWORD", "password")
database = os.getenv("ANSIBLE_INVENTORY_MYSQL_DATABASE", "database")
ssl_skip_verify = os.getenv("ANSIBLE_INVENTORY_MYSQL_SSL_SKIP_VERIFY", "")

class Inventory(object):
    def __init__(
        self,
        username,
        password,
        host,
        port,
        database,
        ssl_skip_verify,
    ):
        self.inventory = {"group":{}, "_meta": {}}
        ssl_verify = False if len(ssl_skip_verify) > 0 else True
        try:
            self.conn = mysql.connector.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=database,
                ssl_verify_identity=ssl_verify,
            )
        except mysql.connector.Error as err:
            print(f"unable to connect to MySQL server: {err}")

    def generate(self):
        """
        generate inventory from MySQL connection
        """
        query = "SELECT * from server_physique;"
        with self.conn.cursor(dictionary=True) as cur:
            cur.execute(query)
            res = cur.fetchall()
        self.inventory["group"]["hosts"] = []
        self.inventory["_meta"]["hostvars"] = {}
        for server in res:
            hostname = server.pop("hostname")
            self.inventory["group"]["hosts"].append(hostname)
            self.inventory["_meta"]["hostvars"][hostname] = server
            self.inventory["_meta"]["hostvars"][hostname]["ansible_host"] = \
                server.get("baseuri")
            
        return json.dumps(self.inventory, indent=2)

    def _empty_inventory(self):
            return {"_meta": {"hostvars": {}}}


if __name__ == "__main__":
    try:
        i = Inventory(
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
            ssl_skip_verify=ssl_skip_verify
        )
        print(i.generate())
    except:
        pass
