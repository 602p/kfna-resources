#!/bin/bash
set -e
rm -rf public
zola build
rsync -Pru --delete public/ hylaea:/var/www/kfna/
