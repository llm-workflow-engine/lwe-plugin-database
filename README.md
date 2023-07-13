# LLM Workflow Engine (LWE) Database plugin

Database plugin for [LLM Workflow Engine](https://github.com/llm-workflow-engine/llm-workflow-engine)

Send natural language commands to a database

**WARNING: POTENTIALLY DANGEROUS -- DATA INTEGRITY CANNOT BE GUARANTEED.**

## Installation

### From packages

Install the latest version of this software directly from github with pip:

```bash
pip install git+https://github.com/llm-workflow-engine/lwe-plugin-database
```

### From source (recommended for development)

Install the latest version of this software directly from git:

```bash
git clone https://github.com/llm-workflow-engine/lwe-plugin-database.git
```

Install the development package:

```bash
cd llm-workflow-engine
pip install -e .
```

## Configuration

Add the following to `config.yaml` in your profile:

```yaml
plugins:
  enabled:
    - database
    # Any other plugins you want enabled...
  # These are the default values.
  database:
    agent:
      verbose: true
    database:
      default: null
```

## Usage

From a running LWE shell:

```
/database connect sqlite:///test.db
/database List all tables in the database
/database disconnect
```
