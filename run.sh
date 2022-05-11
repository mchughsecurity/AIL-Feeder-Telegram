#!/bin/sh

sudo docker run -it --rm --name ail-feeder-telegram --env-file=.env --network=host ail-feeder-telegram