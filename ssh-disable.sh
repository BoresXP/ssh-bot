#!/bin/bash

nft flush chain inet firewall ssh
nft add rule inet firewall ssh drop

