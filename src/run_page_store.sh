export QUART_APP=page_store
export SITERUMMAGE_PAGESTORE_CONFIG=../sample_configs/page_store/config.json
export SITERUMMAGE_PAGESTORE_MESSAGING_CONFIG=../sample_configs/page_store/messaging_queue.json
python -m quart run -p 2020