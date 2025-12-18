#include <mysql/mysql.h>
#include <iostream>
#include <string>


struct MysqlInfo
{
    std::string server_ip = "192.168.103.172", username = "mc", passwd = "mc";
    std::string db_name = "Mydata";
    unsigned int port = 3306;
};
