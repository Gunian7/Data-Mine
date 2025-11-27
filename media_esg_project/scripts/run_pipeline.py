"""Run example pipeline from scripts folder
"""
import argparse
from pathlib import Path
from src.media_esg.pipeline import run_pipeline


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run media ESG pipeline')
    parser.add_argument('--config', required=False, help='Path to pipeline config YAML', default='scripts/config_example.yml')
    args = parser.parse_args()

    print('Running pipeline with config:', args.config)
    run_pipeline(args.config)
