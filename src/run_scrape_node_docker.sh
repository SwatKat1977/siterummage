export SITERUMMAGE_SCRAPENODE_CONFIG=../sample_configs/scrape_node/config.docker.json
export SITERUMMAGE_SCRAPENODE_MESSAGING_CONFIG=../sample_configs/scrape_node/messaging_queue.docker.json
export SITERUMMAGE_SCRAPENODE_PORT=9090
python scrape_node/scrape_node.py
