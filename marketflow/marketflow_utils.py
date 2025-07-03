"""
Shared Utility Functions for the Marketflow Project

This module contains common, reusable functions that are shared across different
modules to avoid code duplication and maintain a single source of truth.
"""

from pathlib import Path

def get_project_root() -> Path:
    """Get the project root directory by locating the '.marketflow' marker."""
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if (parent / ".marketflow").exists():
            return parent
    # Fallback to the parent directory of the 'marketflow' package
    return Path(__file__).parent.parent