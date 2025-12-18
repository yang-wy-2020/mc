# 拉取 MySQL 5.7 镜像
docker pull mysql:5.7

docker stop mc_mysql && docker rm mc_mysql

# 运行容器
docker run -d \
  --name mc_mysql \
  --network host \
  -e MYSQL_ROOT_PASSWORD=123 \
  -p 3306:3306 \
  -v ~/.mysql/:/var/lib/mysql \
  -v ~/workspace/github/mc:/debug/mc \
  -w /debug \
  mysql:5.7 \
  --character-set-server=utf8mb4 \
  --collation-server=utf8mb4_unicode_ci
