#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import Error


class SQL:
    def __init__(self, host: str, user: str, password: str, database: str, table: str) -> None:
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = 3306
        self.table = table
        self.conn = None
        self.charset = 'utf8mb4'
        self.cursor = None

    def connect(self) -> bool:
        """connect to the database"""
        print("connecting to database...")
        try:
            self.conn = mysql.connector.connect(
                host=self.host, 
                user=self.user, 
                password=self.password, 
                database=self.database,
                port=self.port,
                charset=self.charset
            )
            self.cursor = self.conn.cursor()
            print("connect to database successfully")
            return True
        except Error as e:
            print(f"disconnect: {e}")
            return False

    def close(self) -> None:
        """close the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("connection closed")
    
    ###  insert wardrobe 
    def insertOnce(self, type_val, temperature=None, price=None) -> None:
        """insert a single wardrobe into the database"""
        try:
            sql = "INSERT INTO wardrobe (type, temperature, price) VALUES (%s, %s, %s)"
            values = (type_val, temperature, price)
            self.cursor.execute(sql, values)
            self.conn.commit()
            print(f"type:{type_val}, temp:{temperature}, price:{price} inserted successfully")
        except Error as e:
            print(f"insertOnce error: {e}")
    #### end

    ###  delete wardrobe 
    def deleteByType(self, type_val: str) -> None:
        """delete wardrobe by type from the database"""
        print("deleting wardrobe by type...")
        try:
            sql = "DELETE FROM wardrobe WHERE type = %s"
            self.cursor.execute(sql, (type_val,))
            self.conn.commit()
            print(f"wardrobe of type '{type_val}' deleted successfully")
        except Error as e:
            print(f"deleteByType error: {e}")

    def deleteById(self, id_val: int) -> None:
        """delete wardrobe by id from the database"""
        print("deleting wardrobe by id...")
        try:
            sql = "DELETE FROM wardrobe WHERE id = %s"
            self.cursor.execute(sql, (id_val,))
            self.conn.commit()
            print(f"wardrobe with id '{id_val}' deleted successfully")
        except Error as e:
            print(f"deleteById error: {e}")
    
    def deleteByTimestamp(self, days=30) -> None:
        """delete wardrobe older than specified days from the database"""
        print("deleting wardrobe by timestamp...")
        try:
            sql = "DELETE FROM wardrobe WHERE timestamp < NOW() - INTERVAL %s DAY"
            self.cursor.execute(sql, (days,))
            self.conn.commit()
            print(f"wardrobe older than '{days}' days deleted successfully")
        except Error as e:
            print(f"deleteByTimestamp error: {e}")
    
    def deleteAll(self) -> None:
        """delete all wardrobe from the database"""
        print("deleting all wardrobe...")
        try:
            sql = "DELETE FROM wardrobe"
            self.cursor.execute(sql)
            self.conn.commit()
            print("all wardrobe deleted successfully")
        except Error as e:
            print(f"deleteAll error: {e}")
    #### end 
    
    ### update wardrobe
    def updateByTemporature(self, record_id: int, new_temperature: float) -> None:
        """update wardrobe by id with new temperature"""
        print("updating wardrobe by id with new temperature...")
        try:
            sql = "UPDATE wardrobe SET temperature = %s WHERE id = %s"
            self.cursor.execute(sql, (new_temperature, record_id))
            self.conn.commit()
            print(f"wardrobe with id '{record_id}' updated successfully")
        except Error as e:
            print(f"updateByTemporature error: {e}")

    def updateByPrice(self, record_id: int, new_price: float) -> None: 
        """update wardrobe by id with new price"""
        print("updating wardrobe by id with new price...")
        try:
            sql = "UPDATE wardrobe SET price = %s WHERE id = %s"
            self.cursor.execute(sql, (new_price, record_id))
            self.conn.commit()
            print(f"wardrobe with id '{record_id}' updated successfully")
        except Error as e:
            print(f"updateByPrice error: {e}")

    def updateByMultiple(self, record_id, new_type=None, new_temperature=None, new_price=None) -> None:
        """update wardrobe by id with multiple fields"""
        print("updating wardrobe by id with multiple fields...")
        try:
            fields = []
            values = []
            if new_type is not None:
                fields.append("type = %s")
                values.append(new_type)
            if new_temperature is not None:
                fields.append("temperature = %s")
                values.append(new_temperature)
            if new_price is not None:
                fields.append("price = %s")
                values.append(new_price)
            values.append(record_id)
            sql = f"UPDATE wardrobe SET {', '.join(fields)} WHERE id = %s"
            self.cursor.execute(sql, tuple(values))
            self.conn.commit()
            print(f"wardrobe with id '{record_id}' updated successfully")
        except Error as e:
            print(f"updateByMultiple error: {e}")
    #### end

    ### select wardrobe
    def selectByType(self, type_val: str) -> list:
        """select wardrobe by type from the database"""
        try:
            sql = "SELECT * FROM wardrobe WHERE type = %s ORDER BY timestamp DESC"
            self.cursor.execute(sql, (type_val,))
            results = self.cursor.fetchall()
            print(f"Selected {len(results)} records of type '{type_val}'")
            return results
        except Error as e:
            print(f"selectByType error: {e}")
            return []

    def selectById(self, id_val: int) -> list:
        """select wardrobe by id from the database"""
        try:
            sql = "SELECT * FROM wardrobe WHERE id = %s"
            self.cursor.execute(sql, (id_val,))
            results = self.cursor.fetchall()
            print(f"Selected {len(results)} records with id '{id_val}'")
            return results
        except Error as e:
            print(f"selectById error: {e}")
            return []

    def selectAllInformation(self, limit: int = 20) -> list:
        """select all wardrobe from the database"""
        try:
            sql = "SELECT * FROM wardrobe ORDER BY timestamp DESC LIMIT %s"
            self.cursor.execute(sql, (limit,))
            results = self.cursor.fetchall()
            
            print(f"\n{'='*60}")
            print(f"查询结果（最近{limit}条）:")
            print(f"{'ID':<5} {'类型':<10} {'温度':<8} {'价格':<10} {'时间':<20}")
            print("-" * 60)

            for row in results:
                id_val, time_val, type_val, temp_val, price_val = row
                time_str = time_val.strftime("%Y-%m-%d %H:%M:%S")
                temp_str = f"{temp_val:.1f}℃" if temp_val else "NULL"
                price_str = f"¥{price_val:.2f}" if price_val else "NULL"
                print(f"{id_val:<5} {type_val:<10} {temp_str:<8} {price_str:<10} {time_str:<20}")
            print("=" * 60)
            return results
        except Error as e:
            print(f"selectAllInformation error: {e}")
            return []
    #### end