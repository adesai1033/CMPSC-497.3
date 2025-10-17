#!/usr/bin/env python3
"""
Fix Jupyter notebook widget metadata for GitHub rendering.
GitHub expects metadata.widgets to have a top-level 'state' key.
"""
import json
import sys
from pathlib import Path


def fix_notebook_widgets(notebook_path):
    """Remove problematic widgets metadata from Jupyter notebook for GitHub compatibility."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Check if metadata.widgets exists
    if 'metadata' not in notebook:
        print(f"No metadata found in {notebook_path}")
        return False
    
    if 'widgets' not in notebook['metadata']:
        print(f"No widgets metadata found in {notebook_path}")
        return False
    
    # Remove the widgets metadata entirely - it causes GitHub rendering issues
    # The widget outputs in cells will still be preserved
    del notebook['metadata']['widgets']
    
    # Write back to file
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
        f.write('\n')  # Add trailing newline
    
    print(f"✓ Removed widgets metadata from {notebook_path}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_notebook_widgets.py <notebook1.ipynb> [notebook2.ipynb ...]")
        sys.exit(1)
    
    fixed_count = 0
    for notebook_path in sys.argv[1:]:
        path = Path(notebook_path)
        if not path.exists():
            print(f"✗ File not found: {notebook_path}")
            continue
        
        if path.suffix != '.ipynb':
            print(f"✗ Not a notebook file: {notebook_path}")
            continue
        
        if fix_notebook_widgets(path):
            fixed_count += 1
    
    print(f"\n{fixed_count} notebook(s) fixed")


if __name__ == '__main__':
    main()
