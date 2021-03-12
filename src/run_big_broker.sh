export QUART_APP=big_broker
export SITERUMMAGE_BIGBROKER_CONFIG=../sample_configs/big_broker/config.json
export SITERUMMAGE_BIGBROKER_MESSAGING_CONFIG=../sample_configs/big_broker/messaging_queue.json
python -m quart run -p 3232