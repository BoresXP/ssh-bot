#!/bin/bash

nft insert rule inet firewall ssh position 0 ip saddr $REMOTE_IP tcp dport ssh accept 

