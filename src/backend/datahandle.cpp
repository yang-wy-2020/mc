#include "datahandle.h"

int main() {
    MYSQL *conn;
    MYSQL_RES *res;
    MYSQL_ROW row;
    
    // 初始化连接
    conn = mysql_init(NULL);
    
    MysqlInfo *conn_info;

    if (!conn) {
        std::cerr << "mysql_init() failed" << std::endl;
        return 1;
    }
    
    // 连接到数据库
    // 参数：连接句柄, 主机名, 用户名, 密码, 数据库名, 端口, Unix套接字, 客户端标志
    if (!mysql_real_connect(conn, conn_info->server_ip, conn_info->username, conn_info->passwd, 
                           conn_info->db_name, conn_info->port, NULL, 0)) {
        std::cerr << "连接失败: " << mysql_error(conn) << std::endl;
        return 1;
    }
    
    // 设置字符集为UTF-8
    mysql_set_character_set(conn, "utf8");
    
    // 插入数据的SQL语句
    std::string sql = "INSERT INTO users (name, email, age) VALUES ('John Doe', 'john@example.com', 25)";
    
    // 执行SQL语句
    if (mysql_query(conn, sql.c_str())) {
        std::cerr << "插入失败: " << mysql_error(conn) << std::endl;
        return 1;
    }
    
    // 获取受影响的行数
    my_ulonglong affected_rows = mysql_affected_rows(conn);
    std::cout << "插入了 " << affected_rows << " 行数据" << std::endl;
    
    // 获取自增ID（如果有自增主键）
    my_ulonglong insert_id = mysql_insert_id(conn);
    std::cout << "自增ID: " << insert_id << std::endl;
    
    // 关闭连接
    mysql_close(conn);
    
    return 0;
}