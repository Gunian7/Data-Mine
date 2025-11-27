"""media_esg package
"""
__all__ = ["run_pipeline"]

def run_pipeline(*args, **kwargs):
	"""Lazy-load pipeline runner to avoid heavy imports on package import.
	"""
	from .pipeline import run_pipeline as _run_pipeline
	return _run_pipeline(*args, **kwargs)
