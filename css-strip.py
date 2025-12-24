#!/usr/bin/env python3
import sys
from pathlib import Path
import tinycss2
import argparse

def serialize_rule(rule):
    if rule.type == 'qualified-rule':
        return tinycss2.serialize([rule])
    else:
        return rule.serialize()

def strip_tokens(tokens, remove_selectors, keep_selectors):
    """
    Remove rules containing any of the remove_selectors,
    unless they also contain a keep selector.
    Also removes :not(remove_selector) from selectors.
    """
    out_tokens = []

    for t in tokens:
        if t.type == 'qualified-rule':
            sel_text = tinycss2.serialize(t.prelude)

            # Remove :not(remove_selector) for each selector to remove
            for rs in remove_selectors:
                sel_text = sel_text.replace(f':not({rs})', '')

            # Check if rule should be kept
            has_remove = any(rs in sel_text for rs in remove_selectors)
            has_keep = any(ks in sel_text for ks in keep_selectors)

            if has_remove and not has_keep:
                continue  # skip this rule

            # Update prelude tokens if modified
            if sel_text != tinycss2.serialize(t.prelude):
                t.prelude = tinycss2.parse_component_value_list(sel_text)

            out_tokens.append(t)
        else:
            out_tokens.append(t)  # preserve comments, whitespace, at-rules
    return out_tokens

def process_file(path, remove_selectors, keep_selectors):
    css_text = path.read_text(encoding='utf-8')

    # Parse everything including whitespace and comments
    tokens = tinycss2.parse_rule_list(css_text, skip_comments=False, skip_whitespace=False)

    # Write normalized version
    normalized_path = path.with_suffix('.normalized.css')
    normalized_css = ''.join([serialize_rule(t) for t in tokens])
    normalized_path.write_text(normalized_css, encoding='utf-8')

    # Strip tokens
    stripped_tokens = strip_tokens(tokens, remove_selectors, keep_selectors)

    # Write stripped version
    stripped_path = path.with_suffix('.stripped.css')
    stripped_css = ''.join([serialize_rule(t) for t in stripped_tokens])
    stripped_path.write_text(stripped_css, encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description="Strip CSS rules safely from GTK CSS files")
    parser.add_argument('css_files', nargs='+', help='CSS files to process')
    parser.add_argument('--remove', action='append', default=[], help='Selector to remove (can be used multiple times)')
    parser.add_argument('--keep', action='append', default=[], help='Selector to preserve (can be used multiple times)')
    args = parser.parse_args()

    for css_file in args.css_files:
        path = Path(css_file)
        if not path.is_file():
            print(f"File not found: {css_file}", file=sys.stderr)
            continue
        process_file(path, args.remove, args.keep)

if __name__ == "__main__":
    main()
