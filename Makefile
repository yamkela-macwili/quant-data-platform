.PHONY: help install ingest pipeline test clean

PYTHON = python3
EXPORT_PATH = PYTHONPATH=.

help:
	@echo "Quant Data Platform"
	@echo ""
	@echo "Setup:"
	@echo "  make install     Install Python dependencies"
	@echo ""
	@echo "Pipeline:"
	@echo "  make ingest      Download raw BTCUSDT data from Binance"
	@echo "  make pipeline    Run full pipeline (ingest → process → features → reports)"
	@echo ""
	@echo "Testing:"
	@echo "  make test        Run all tests"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean       Remove generated data and reports"

install:
	$(PYTHON) -m pip install -r requirements.txt

ingest:
	$(EXPORT_PATH) $(PYTHON) scripts/ingest_btc.py

pipeline:
	$(EXPORT_PATH) $(PYTHON) scripts/run_pipeline.py

test:
	$(EXPORT_PATH) $(PYTHON) -m pytest tests/ -v

clean:
	rm -rf data/raw/*.parquet data/raw/*.csv
	rm -rf data/processed/*.parquet data/processed/*.csv
	rm -rf reports/*.png reports/*.csv
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
