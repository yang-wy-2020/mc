# build 

docker build  --no-cache  -f ./Dockerfile --build-arg HTTP_PROXY=http://proxy.qomolo.com:8123/  --build-arg HTTPS_PROXY=http://proxy.qomolo.com:8123/ --build-arg ALL_PROXY=http://proxy.qomolo.com:8123/ -t mysql_mc:v0.1 -
