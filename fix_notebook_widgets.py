#!/usr/bin/env python3
"""
Fix Jupyter notebook widget metadata for GitHub rendering.
GitHub expects metadata.widgets to have a top-level 'state' key.
"""
import json
import sys
from pathlib import Path


def fix_notebook_widgets(notebook_path):
    """Fix the widgets metadata structure in a Jupyter notebook."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Check if metadata.widgets exists
    if 'metadata' not in notebook:
        print(f"No metadata found in {notebook_path}")
        return False
    
    if 'widgets' not in notebook['metadata']:
        print(f"No widgets metadata found in {notebook_path}")
        return False
    
    widgets = notebook['metadata']['widgets']
    
    # Check if it already has the correct structure
    if 'state' in widgets and isinstance(widgets['state'], dict):
        print(f"✓ {notebook_path} already has correct structure")
        return False
    
    # If widgets is a dict with widget IDs, restructure it
    if isinstance(widgets, dict) and widgets:
        # Check if this looks like the old structure (has widget IDs as keys)
        first_key = next(iter(widgets.keys()))
        if first_key != 'state' and isinstance(widgets[first_key], dict):
            # Restructure: wrap existing widgets in a 'state' key
            notebook['metadata']['widgets'] = {
                'state': widgets
            }
            
            # Write back to file
            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=1, ensure_ascii=False)
                f.write('\n')  # Add trailing newline
            
            print(f"✓ Fixed {notebook_path}")
            return True
    
    print(f"⚠ {notebook_path} has unexpected widgets structure")
    return False


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
