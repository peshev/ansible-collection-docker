#!/usr/bin/env bash

PAGES=(
  "install/ubuntu"
  "install/debian"
  "install/rhel"
  "install/fedora"
  "install/centos"
  "install/linux-postinstall"
  "logging/drivers/json-file"
  "network/firewall-nftables"
  "swarm/swarm-mode"
  "daemon"
)
DOCS_DIR=$(realpath $(dirname $0)/../docs)
for page in ${PAGES[@]}; do
  mkdir -p $DOCS_DIR/$(dirname $page)
  curl https://docs.docker.com/engine/$page.md -o $DOCS_DIR/$page.md
done