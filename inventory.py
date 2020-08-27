#!/usr/bin/env python

import os
import json

import mysql.connector

# MySQL server connection information
# TODO: could be loaded from a configuration file
host = os.getenv("ANSIBLE_INVENTORY_MYQSL_HOST", "localhost")
port = os.getenv("ANSIBLE_INVENTORY_MYSQL_PORT", 3306)
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
        # define base inventory
        self.inventory = {"group":{}, "_meta": {}}
        # disable or not SSL CA verification
        ssl_verify = not ssl_skip_verify
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
        query = "SELECT * FROM server_physique;"
        with self.conn.cursor(dictionary=True) as cur:
            cur.execute(query)
            # fetchall will return a dictionary,
            # each column is a key of the dictionary
            res = cur.fetchall()
        # prepare the default group
        self.inventory["group"]["hosts"] = []
        self.inventory["_meta"]["hostvars"] = {}
        for server in res:
            # we save and remove the `hostname` from the
            # json. It's removed to avoid having `hostname`
            # in the hostvars
            hostname = server.pop("hostname")
            self.inventory["group"]["hosts"].append(hostname)
            # we add the server information to hostvars
            self.inventory["_meta"]["hostvars"][hostname] = server
            # custom override to set the `ansible_host` to the baseuri in order
            # to connect
            self.inventory["_meta"]["hostvars"][hostname]["ansible_host"] = \
                server.get("baseuri")
        return json.dumps(self.inventory, indent=2)

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
        # TODO: handle the error
        pass
