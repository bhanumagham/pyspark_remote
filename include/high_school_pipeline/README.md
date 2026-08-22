# High School Pipeline

## Overview

The High School Pipeline is a data processing module within the pyspark_remote project. It provides ETL (Extract, Transform, Load) capabilities for handling and analyzing high school education data.

## Purpose

This pipeline is designed to:
- Extract high school education data from various sources
- Transform and clean the data for analysis
- Load processed data into target systems
- Enable scalable distributed processing using PySpark

## Directory Structure

```
include/high_school_pipeline/
├── README.md          # This file
├── config/            # Configuration files
├── main.py            # Entry point for running the pipeline
├── src/               # Source modules (jobs, transformations, utils, etc.)
└── tests/             # Unit and integration tests
```

> Note: The repository layout places implementation files under `src/` rather than a top-level `jobs/` directory. If you prefer `jobs/`, we can move or add a directory and update imports accordingly.

## Getting Started

### Prerequisites

- Python 3.7+
- PySpark (as specified in the project requirements)
- Docker (optional, for containerized execution)

### Installation

```bash
# Clone the repository
git clone https://github.com/bhanumagham/pyspark_remote.git
cd pyspark_remote

# Install dependencies
pip install -r requirements.txt
```

### Running the Pipeline

```bash
# Execute the pipeline
spark-submit include/high_school_pipeline/main.py

# Or with specific parameters
spark-submit include/high_school_pipeline/main.py --config include/high_school_pipeline/config/production.yaml
```

## Configuration

Configuration files are located in the `include/high_school_pipeline/config/` directory. Modify these files to customize:
- Data source connections
- Output destinations
- Processing parameters
- Environment-specific settings

## Development

### Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly with sample data
4. Submit a pull request

### Testing

```bash
pytest tests/high_school_pipeline/ -v
```

## Project Context

This module is part of the **pyspark_remote** project, which provides a remote repository setup for local PySpark environments.

**Project Composition:**
- 84.6% Jupyter Notebooks
- 15% Python
- 0.4% Docker

## Support

For issues or questions, please refer to the main project repository or open an issue on GitHub.

## License

See the main project LICENSE file for details.
