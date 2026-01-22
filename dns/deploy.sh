#!/bin/bash 

CONTAINER_NAME="dnsmasq"

if [ "$(docker ps -q -f name=${CONTAINER_NAME})" ]; then
    echo "${CONTAINER_NAME} container is already running."
    docker stop ${CONTAINER_NAME}
    docker rm ${CONTAINER_NAME}
    exit 0
fi

DNSMASQ_CONFIG="~/dnsmasq-config/dnsmasq.conf"

if [ -f ${DNSMASQ_CONFIG} ]; then
    echo "config is found, deploying dnsmasq container..."
else
    cp -r -v ./dnsmasq_config ~/dnsmasq-config
fi

docker run -d --name ${CONTAINER_NAME} \
    --restart always \
    -p 53:53/udp \
    -p 53:53/tcp \
    -v ${DNSMASQ_CONFIG}:/etc/dnsmasq.conf \
    --cap-add=NET_ADMIN \
    jpillora/dnsmasq