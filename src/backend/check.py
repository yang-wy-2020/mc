import mysql.connector
from mysql.connector import Error

class WardrobeDB:
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """连接数据库"""
        try:
            self.conn = mysql.connector.connect(
                host='192.168.103.172',
                user='mc',
                password='mc',
                database='Mydata',
                port=3306,
                charset='utf8mb4'
            )
            self.cursor = self.conn.cursor()
            print("✓ 数据库连接成功")
            return True
        except Error as e:
            print(f"❌ 连接失败: {e}")
            return False
    
    def close(self):
        """关闭连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("✓ 数据库连接已关闭")
    
    # ============== 插入操作 ==============
    def insert_one(self, type_val, temperature=None, price=None):
        """插入一条记录"""
        try:
            if temperature is not None and price is not None:
                sql = "INSERT INTO wardrobe (type, temperature, price) VALUES (%s, %s, %s)"
                values = (type_val, float(temperature), float(price))
            elif temperature is not None:
                sql = "INSERT INTO wardrobe (type, temperature) VALUES (%s, %s)"
                values = (type_val, float(temperature))
            elif price is not None:
                sql = "INSERT INTO wardrobe (type, price) VALUES (%s, %s)"
                values = (type_val, float(price))
            else:
                sql = "INSERT INTO wardrobe (type) VALUES (%s)"
                values = (type_val,)
            
            self.cursor.execute(sql, values)
            self.conn.commit()
            print(f"✓ 插入成功，新记录ID: {self.cursor.lastrowid}")
            return self.cursor.lastrowid
        except Error as e:
            print(f"❌ 插入失败: {e}")
            return None
    
    def insert_batch(self, data_list):
        """批量插入记录"""
        try:
            sql = "INSERT INTO wardrobe (type, temperature, price) VALUES (%s, %s, %s)"
            self.cursor.executemany(sql, data_list)
            self.conn.commit()
            print(f"✓ 批量插入成功，共{self.cursor.rowcount}条记录")
            return True
        except Error as e:
            print(f"❌ 批量插入失败: {e}")
            return False
    
    # ============== 查询操作 ==============
    def select_all(self, limit=10):
        """查询所有记录"""
        try:
            sql = "SELECT * FROM wardrobe ORDER BY timestamp DESC LIMIT %s"
            self.cursor.execute(sql, (limit,))
            rows = self.cursor.fetchall()
            
            print(f"\n{'='*60}")
            print(f"查询结果（最近{limit}条）:")
            print(f"{'ID':<5} {'类型':<10} {'温度':<8} {'价格':<10} {'时间':<20}")
            print("-" * 60)
            
            for row in rows:
                id_val, time_val, type_val, temp_val, price_val = row
                time_str = time_val.strftime("%Y-%m-%d %H:%M:%S")
                temp_str = f"{temp_val:.1f}℃" if temp_val else "NULL"
                price_str = f"¥{price_val:.2f}" if price_val else "NULL"
                
                print(f"{id_val:<5} {type_val:<10} {temp_str:<8} {price_str:<10} {time_str:<20}")
            
            print("=" * 60)
            return rows
        except Error as e:
            print(f"❌ 查询失败: {e}")
            return []
    
    def select_by_id(self, record_id):
        """根据ID查询记录"""
        try:
            sql = "SELECT * FROM wardrobe WHERE id = %s"
            self.cursor.execute(sql, (record_id,))
            row = self.cursor.fetchone()
            
            if row:
                print(f"\n✓ 找到记录 ID={record_id}:")
                print(f"  类型: {row[2]}, 温度: {row[3]}, 价格: {row[4]}, 时间: {row[1]}")
                return row
            else:
                print(f"⚠ 未找到 ID={record_id} 的记录")
                return None
        except Error as e:
            print(f"❌ 查询失败: {e}")
            return None
    
    def select_by_type(self, type_val):
        """根据类型查询记录"""
        try:
            sql = "SELECT * FROM wardrobe WHERE type = %s ORDER BY timestamp DESC"
            self.cursor.execute(sql, (type_val,))
            rows = self.cursor.fetchall()
            
            if rows:
                print(f"\n✓ 找到 {len(rows)} 条类型为 '{type_val}' 的记录:")
                for row in rows:
                    print(f"  ID:{row[0]}, 温度:{row[3]}, 价格:{row[4]}, 时间:{row[1]}")
            else:
                print(f"⚠ 未找到类型为 '{type_val}' 的记录")
            
            return rows
        except Error as e:
            print(f"❌ 查询失败: {e}")
            return []
    
    # ============== 更新操作 ==============
    def update_temperature(self, record_id, new_temperature):
        """更新温度字段"""
        try:
            # 先检查记录是否存在
            self.select_by_id(record_id)
            
            sql = "UPDATE wardrobe SET temperature = %s WHERE id = %s"
            self.cursor.execute(sql, (float(new_temperature), record_id))
            self.conn.commit()
            
            if self.cursor.rowcount > 0:
                print(f"✓ 成功更新记录 ID={record_id} 的温度为 {new_temperature}℃")
                return True
            else:
                print(f"⚠ 未更新任何记录，请检查ID是否正确")
                return False
        except Error as e:
            print(f"❌ 更新失败: {e}")
            return False
    
    def update_price(self, record_id, new_price):
        """更新价格字段"""
        try:
            # 先检查记录是否存在
            self.select_by_id(record_id)
            
            sql = "UPDATE wardrobe SET price = %s WHERE id = %s"
            self.cursor.execute(sql, (float(new_price), record_id))
            self.conn.commit()
            
            if self.cursor.rowcount > 0:
                print(f"✓ 成功更新记录 ID={record_id} 的价格为 ¥{new_price:.2f}")
                return True
            else:
                print(f"⚠ 未更新任何记录，请检查ID是否正确")
                return False
        except Error as e:
            print(f"❌ 更新失败: {e}")
            return False
    
    def update_multiple(self, record_id, new_type=None, new_temperature=None, new_price=None):
        """更新多个字段"""
        try:
            # 构建动态SQL
            updates = []
            values = []
            
            if new_type is not None:
                updates.append("type = %s")
                values.append(new_type)
            
            if new_temperature is not None:
                updates.append("temperature = %s")
                values.append(float(new_temperature))
            
            if new_price is not None:
                updates.append("price = %s")
                values.append(float(new_price))
            
            if not updates:
                print("⚠ 没有提供任何更新字段")
                return False
            
            # 添加WHERE条件
            values.append(record_id)
            
            sql = f"UPDATE wardrobe SET {', '.join(updates)} WHERE id = %s"
            self.cursor.execute(sql, tuple(values))
            self.conn.commit()
            
            if self.cursor.rowcount > 0:
                print(f"✓ 成功更新记录 ID={record_id}")
                return True
            else:
                print(f"⚠ 未更新任何记录，请检查ID是否正确")
                return False
        except Error as e:
            print(f"❌ 更新失败: {e}")
            return False
    
    # ============== 删除操作 ==============
    def delete_by_id(self, record_id):
        """根据ID删除记录"""
        try:
            # 先显示要删除的记录
            print(f"\n⚠ 将要删除的记录:")
            self.select_by_id(record_id)
            
            # 确认（在实际应用中，这里可以添加用户确认）
            confirm = input("确定要删除这条记录吗？(y/n): ").strip().lower()
            if confirm != 'y':
                print("操作已取消")
                return False
            
            sql = "DELETE FROM wardrobe WHERE id = %s"
            self.cursor.execute(sql, (record_id,))
            self.conn.commit()
            
            if self.cursor.rowcount > 0:
                print(f"✓ 成功删除记录 ID={record_id}")
                return True
            else:
                print(f"⚠ 未删除任何记录，请检查ID是否正确")
                return False
        except Error as e:
            print(f"❌ 删除失败: {e}")
            return False
    
    def delete_by_type(self, type_val):
        """根据类型删除记录"""
        try:
            # 先显示要删除的记录
            print(f"\n⚠ 将要删除类型为 '{type_val}' 的所有记录:")
            self.select_by_type(type_val)
            
            # 确认
            confirm = input(f"确定要删除所有类型为 '{type_val}' 的记录吗？(y/n): ").strip().lower()
            if confirm != 'y':
                print("操作已取消")
                return False
            
            sql = "DELETE FROM wardrobe WHERE type = %s"
            self.cursor.execute(sql, (type_val,))
            self.conn.commit()
            
            deleted_count = self.cursor.rowcount
            print(f"✓ 成功删除 {deleted_count} 条类型为 '{type_val}' 的记录")
            return True
        except Error as e:
            print(f"❌ 删除失败: {e}")
            return False
    
    def delete_old_records(self, days=30):
        """删除指定天数前的记录"""
        try:
            sql = "DELETE FROM wardrobe WHERE timestamp < DATE_SUB(NOW(), INTERVAL %s DAY)"
            self.cursor.execute(sql, (days,))
            self.conn.commit()
            
            deleted_count = self.cursor.rowcount
            print(f"✓ 成功删除 {deleted_count} 条 {days} 天前的记录")
            return True
        except Error as e:
            print(f"❌ 删除失败: {e}")
            return False
    
    def delete_all(self):
        """删除所有记录（危险操作）"""
        try:
            # 先显示所有记录
            self.select_all(limit=20)
            
            # 再次确认
            confirm1 = input("\n⚠⚠⚠ 警告：这将删除所有记录！确定继续吗？(y/n): ").strip().lower()
            if confirm1 != 'y':
                print("操作已取消")
                return False
            
            confirm2 = input("请再次确认，输入 'DELETE ALL' 继续: ").strip()
            if confirm2 != 'DELETE ALL':
                print("操作已取消")
                return False
            
            sql = "DELETE FROM wardrobe"
            self.cursor.execute(sql)
            self.conn.commit()
            
            deleted_count = self.cursor.rowcount
            print(f"✓ 已删除所有记录，共 {deleted_count} 条")
            
            # 重置自增ID（可选）
            reset_sql = "ALTER TABLE wardrobe AUTO_INCREMENT = 1"
            self.cursor.execute(reset_sql)
            self.conn.commit()
            print("✓ 已重置自增ID")
            return True
        except Error as e:
            print(f"❌ 删除失败: {e}")
            return False
    
    # ============== 统计操作 ==============
    def get_statistics(self):
        """获取统计信息"""
        try:
            sql = """
            SELECT 
                COUNT(*) as 总记录数,
                COUNT(temperature) as 有温度记录数,
                COUNT(price) as 有价格记录数,
                AVG(temperature) as 平均温度,
                AVG(price) as 平均价格,
                MIN(temperature) as 最低温度,
                MAX(temperature) as 最高温度,
                MIN(price) as 最低价格,
                MAX(price) as 最高价格
            FROM wardrobe
            """
            self.cursor.execute(sql)
            stats = self.cursor.fetchone()
            
            print("\n" + "="*60)
            print("数据库统计信息:")
            print("-" * 60)
            print(f"总记录数: {stats[0]}")
            print(f"有温度记录数: {stats[1]}")
            print(f"有价格记录数: {stats[2]}")
            
            if stats[3]:
                print(f"平均温度: {stats[3]:.1f}℃")
            if stats[4]:
                print(f"平均价格: ¥{stats[4]:.2f}")
            if stats[5] and stats[6]:
                print(f"温度范围: {stats[5]:.1f}℃ ~ {stats[6]:.1f}℃")
            if stats[7] and stats[8]:
                print(f"价格范围: ¥{stats[7]:.2f} ~ ¥{stats[8]:.2f}")
            print("="*60)
            
            return stats
        except Error as e:
            print(f"❌ 统计失败: {e}")
            return None


def demo_all_operations():
    """演示所有操作"""
    db = WardrobeDB()
    
    if not db.connect():
        return
    
    try:
        print("\n" + "="*60)
        print("1. 插入数据演示")
        print("="*60)
        
        # 插入单条数据
        db.insert_one("上衣", 25.5, 299.99)
        db.insert_one("裤子", 26.0, 199.99)
        db.insert_one("外套", 24.5)  # 只插入类型和温度
        
        # 批量插入
        batch_data = [
            ("衬衫", 27.5, 159.99),
            ("裙子", 26.8, 399.99),
            ("毛衣", 28.2, 259.99),
        ]
        db.insert_batch(batch_data)
        
        print("\n" + "="*60)
        print("2. 查询数据演示")
        print("="*60)
        
        # 查询所有记录
        db.select_all(limit=10)
        
        # 按类型查询
        db.select_by_type("上衣")
        
        print("\n" + "="*60)
        print("3. 更新数据演示")
        print("="*60)
        
        # 获取最后插入的ID用于演示更新
        db.cursor.execute("SELECT MAX(id) FROM wardrobe")
        last_id = db.cursor.fetchone()[0]
        
        # 更新温度
        if last_id:
            db.update_temperature(last_id, 30.5)
        
        # 更新价格
        db.update_price(last_id, 349.99)
        
        # 更新多个字段
        db.update_multiple(last_id, new_type="厚外套", new_temperature=22.0, new_price=599.99)
        
        print("\n" + "="*60)
        print("4. 删除数据演示")
        print("="*60)
        
        # 注意：这里注释掉了删除操作，实际使用时取消注释
        # 删除指定ID的记录
        # db.delete_by_id(1)
        
        # 删除指定类型的记录
        # db.delete_by_type("测试类型")
        
        # 删除30天前的记录
        # db.delete_old_records(30)
        
        # 危险：删除所有记录
        # db.delete_all()
        
        print("\n" + "="*60)
        print("5. 统计信息")
        print("="*60)
        
        db.get_statistics()
        
        print("\n✓ 所有操作演示完成")
        
    finally:
        db.close()


def interactive_menu():
    """交互式菜单"""
    db = WardrobeDB()
    
    if not db.connect():
        return
    
    try:
        while True:
            print("\n" + "="*60)
            print("衣物数据库管理系统")
            print("="*60)
            print("1. 插入数据")
            print("2. 查询所有记录")
            print("3. 按ID查询")
            print("4. 按类型查询")
            print("5. 更新温度")
            print("6. 更新价格")
            print("7. 更新多个字段")
            print("8. 按ID删除")
            print("9. 按类型删除")
            print("10. 查看统计")
            print("11. 退出")
            print("-" * 60)
            
            choice = input("请选择操作 (1-11): ").strip()
            
            if choice == "1":
                print("\n[插入数据]")
                type_val = input("衣物类型: ").strip()
                temp_val = input("温度(℃, 可不填): ").strip()
                price_val = input("价格(¥, 可不填): ").strip()
                
                temperature = float(temp_val) if temp_val else None
                price = float(price_val) if price_val else None
                
                db.insert_one(type_val, temperature, price)
                
            elif choice == "2":
                limit = input("显示多少条记录? (默认10): ").strip()
                limit = int(limit) if limit else 10
                db.select_all(limit)
                
            elif choice == "3":
                record_id = input("请输入记录ID: ").strip()
                if record_id.isdigit():
                    db.select_by_id(int(record_id))
                else:
                    print("❌ 请输入有效的数字ID")
                    
            elif choice == "4":
                type_val = input("请输入衣物类型: ").strip()
                db.select_by_type(type_val)
                
            elif choice == "5":
                record_id = input("请输入要更新的记录ID: ").strip()
                new_temp = input("请输入新的温度值(℃): ").strip()
                if record_id.isdigit() and new_temp:
                    db.update_temperature(int(record_id), float(new_temp))
                else:
                    print("❌ 请输入有效的ID和温度值")
                    
            elif choice == "6":
                record_id = input("请输入要更新的记录ID: ").strip()
                new_price = input("请输入新的价格(¥): ").strip()
                if record_id.isdigit() and new_price:
                    db.update_price(int(record_id), float(new_price))
                else:
                    print("❌ 请输入有效的ID和价格")
                    
            elif choice == "7":
                record_id = input("请输入要更新的记录ID: ").strip()
                new_type = input("新的类型(可不填): ").strip() or None
                new_temp = input("新的温度(℃, 可不填): ").strip()
                new_price = input("新的价格(¥, 可不填): ").strip()
                
                temperature = float(new_temp) if new_temp else None
                price = float(new_price) if new_price else None
                
                if record_id.isdigit():
                    db.update_multiple(int(record_id), new_type, temperature, price)
                else:
                    print("❌ 请输入有效的ID")
                    
            elif choice == "8":
                record_id = input("请输入要删除的记录ID: ").strip()
                if record_id.isdigit():
                    db.delete_by_id(int(record_id))
                else:
                    print("❌ 请输入有效的数字ID")
                    
            elif choice == "9":
                type_val = input("请输入要删除的衣物类型: ").strip()
                db.delete_by_type(type_val)
                
            elif choice == "10":
                db.get_statistics()
                
            elif choice == "11":
                print("谢谢使用，再见！")
                break
                
            else:
                print("❌ 无效选择，请重新输入")
                
            input("\n按Enter键继续...")
            
    finally:
        db.close()


if __name__ == "__main__":
    # 选择运行模式
    
    print("请选择运行模式:")
    print("1. 演示所有操作（自动执行插入、查询、更新、删除示例）")
    print("2. 交互式菜单（手动选择操作）")
    
    mode = input("请输入选择 (1或2): ").strip()
    
    if mode == "1":
        demo_all_operations()
    elif mode == "2":
        interactive_menu()
    else:
        print("无效选择，运行演示模式...")
        demo_all_operations()