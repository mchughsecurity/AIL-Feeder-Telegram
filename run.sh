#!/bin/sh

sudo docker run -it --rm --name ail-feeder-telegram --env-file=.env --network=host --mount type=bind,src=`pwd`/storage,dst=/storage ail-feeder-telegram