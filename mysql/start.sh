# 拉取 MySQL 5.7 镜像
docker pull mysql:5.7

docker stop mc_mysql && docker rm mc_mysql

# 运行容器
docker run -d \
  --name mc_mysql \
  -e MYSQL_ROOT_PASSWORD=123 \
  -p 3306:3306 \
  -v ~/.mysql/:/var/lib/mysql \
  mysql:5.7 \
  --character-set-server=utf8mb4 \
  --collation-server=utf8mb4_unicode_ci
