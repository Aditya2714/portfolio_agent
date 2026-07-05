.PHONY: setup run clean

# Setup project
setup:
	pip install -r requirements.txt

# Run Streamlit app
run:
	streamlit run app/streamlit_app.py

# Clean generated files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf data/portfolio.json
