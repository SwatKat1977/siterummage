export QUART_APP=page_store
export SITERUMMAGE_PAGESTORE_CONFIG=../sample_configs/page_store/config.docker.json
export SITERUMMAGE_PAGESTORE_MESSAGING_CONFIG=../sample_configs/page_store/messaging_queue.docker.json
python -m quart run -p 2020