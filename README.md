# AIL-Feeder-Telegram

A newly rewritten AIL Feeder for Telegram conversations.

## Quickstart

1. Clone this repository
2. Copy .env.sample to .env
3. Update variables in .env as appropriate
4. Build through docker-compose build or ./build.sh
5. First start via ./run.sh - follow the prompts
6. After first start, run through docker-compose up -d

## Concept of operations

``This feeder is intended to operate within a Docker environment via docker run or docker-compose.
If you are intending to run this through python3 outside of Docker, the execution will fail.``

On first run through ./run.sh, the Feeder will ask for the service number associated with your Telegram account.
A passcode will be sent to your Telegram client, which needs to be entered into the Feeder script.

Once authenticated, a session file is saved with volume bind to ./storage - the session file name is derived from
parameters in the .env file.

The Feeder will automatically start parsing through all conversations and messages which your Telegram account has
access to, and begin sending the message.text fields, and some metadata into AIL.

Each message the Feeder encounters is added to the Redis cache with an expiry of 86400 seconds. If subsequent runs of the
feeder encounter a previous submitted message, the redis cache is reset to 86400 seconds for that message. This should
prevent duplicate submissions of the same messages within conversations.

Metadata submitted for each message sent to AIL include the t.me/ link to each specific message, and includes the
plaintext included within each message.

There is no current support for attachments, however that will likely be a future feature to be considered.