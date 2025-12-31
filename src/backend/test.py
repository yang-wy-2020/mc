#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sql import SQL  # Assuming sql.py is in the same directory


sql = SQL(
    host='192.168.103.172',
    user='mc',
    password='mc',
    database='Mydata'
)

if sql.connect():
    # Example usage
    sql.selectAllInformation(limit=10)
    # sql.insertOnce(type_val='jacket', temperature=3, price=49.99)
    sql.deleteByType(type_val='jacket')
    # sql.deleteById(id_val=13)
    print("---")
    sql.selectAllInformation(limit=2)
    sql.close()