export QUART_APP=scrape_node
export SITERUMMAGE_SCRAPENODE_CONFIG=../sample_configs/scrape_node/config.json
export SITERUMMAGE_SCRAPENODE_PORT=9090
python -m quart run -p $SITERUMMAGE_SCRAPENODE_PORT
