#!/bin/sh

INTERFACE=$1
SPAN_NETNS=$2

mkdir -p /var/run/netns
ln -s /proc/$SPAN_NETNS/ns/net /var/run/netns/$SPAN_NETNS
ip link set $INTERFACE netns $SPAN_NETNS
ip netns exec $SPAN_NETNS ip link set $INTERFACE up
