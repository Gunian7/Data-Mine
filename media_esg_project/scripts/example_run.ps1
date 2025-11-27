# PowerShell example to run the pipeline with `src` on PYTHONPATH
$env:PYTHONPATH = "$PWD/src"
python .\scripts\run_pipeline.py --config scripts/config_example.yml
