# === Configurable Variables ===
ENV_NAME := conda-faiss-cpu
CONDA_SH := /usr/local/Caskroom/miniconda/base/etc/profile.d/conda.sh
PYTHON_VERSION := 3.10

# === Commands ===

# Step 1: Create Conda env and install faiss
conda-create:
	@echo "🚀 Creating Conda environment: $(ENV_NAME)"
	conda create -y -n $(ENV_NAME) python=$(PYTHON_VERSION)
	@echo "✅ Installing faiss-cpu in Conda env"
	conda run -n $(ENV_NAME) conda install -c conda-forge -y faiss-cpu

# Step 2: Install Pipenv inside Conda
pipenv-install:
	@echo "📦 Installing Pipenv in Conda env $(ENV_NAME)"
	conda run -n $(ENV_NAME) pip install pipenv

# Step 3: Install Pipenv project dependencies
# NOTE - conda run -n ... pipenv must be chained properly 
# - otherwise conda run launches a subprocess that doesn't inherit the pipenv environment properly, especially not with PIPENV_PYTHON
pipenv-deps:
	@echo "📂 Installing Pipenv project dependencies inside Conda environment"
	/bin/bash -c "source $(CONDA_SH) && conda activate $(ENV_NAME) && PIPENV_PYTHON=$(shell which -a python | grep '/envs/$(ENV_NAME)/bin/python' | head -n 1) pipenv install --dev"

# Step 4: Launch Pipenv shell (within Conda)
shell:
	@echo "💻 Entering Pipenv shell within Conda Python $(ENV_NAME)"
	/bin/bash -c "source $(CONDA_SH) && conda activate $(ENV_NAME) && PIPENV_PYTHON=$(shell which -a python | grep '/envs/$(ENV_NAME)/bin/python' | head -n 1) pipenv shell"

# Step 5: Check Python version of nested Conda + Pipenv
check-python:
	@echo "🐍 Pipenv Python location:"
	@conda run -n $(ENV_NAME) pipenv run which python

# Run the FastAPI server
run-api:
	@echo "🚀 Starting FastAPI server"
	/bin/bash -c "source $(CONDA_SH) && conda activate $(ENV_NAME) && pipenv run uvicorn api.main:app --reload --reload-dir api --reload-dir evaluation --reload-dir utils"

# Send a sample eval request to the FastAPI server
send-sample-request:
	@echo "📤 Extracting and sending sample_conversation.json to API..."
	python scripts/send_sample_request.py

# Send n-th conversation to the FastAPI server
send-n:
	@echo "📤 Sending Nth conversation (use: make send-n N=5)"
	python scripts/send_nth_conversation.py $(N)

# Run the Streamlit app
streamlit:
	@echo "📊 Running Streamlit dashboard"
	conda run -n $(ENV_NAME) pipenv run streamlit run cli/streamlit_dashboard.py

# Run tests
test:
	conda run -n $(ENV_NAME) pipenv run pytest --cov=evaluation tests/

# Run code formatters
format:
	conda run -n $(ENV_NAME) pipenv run black .
	conda run -n $(ENV_NAME) pipenv run isort .

# Export dependencies (for CI or Streamlit Cloud)
export-dependencies:
	@echo "📋 Exporting requirements.txt (for Streamlit or CI/CD)"
	conda run -n $(ENV_NAME) pipenv lock -r > requirements.txt

# Check package versions
check:
	@echo "🔎 Checking faiss, torch, and Python version"
	conda run -n $(ENV_NAME) pipenv run python -c "import faiss; print('✅ faiss:', faiss.__version__)"
	conda run -n $(ENV_NAME) pipenv run python -c "import torch; print('✅ torch:', torch.__version__)"
	conda run -n $(ENV_NAME) pipenv run python -V

# Clean Conda + Pipenv setup
clean:
	@echo "🧹 Removing Conda environment: $(ENV_NAME)"
	conda env remove -n $(ENV_NAME)
	rm -f Pipfile.lock requirements.txt
