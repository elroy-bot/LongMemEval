#!/usr/bin/env python3
"""
Script to generate data for LongMemEval.
This script reads a JSON file and processes the questions.
"""

import json
import argparse
import os
from pathlib import Path


def read_data(filename):
    """
    Read the JSON data file and return the parsed content.

    Args:
        filename (str): Path to the JSON file

    Returns:
        list: Parsed JSON data
    """
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def print_questions(data):
    """
    Print each question from the data.

    Args:
        data (list): List of question entries
    """
    for i, entry in enumerate(data):
        print(f"Question {i+1} (ID: {entry['question_id']}):")
        print(f"Type: {entry['question_type']}")
        print(f"Question: {entry['question']}")
        print(f"Answer: {entry['answer']}")
        print(f"Date: {entry['question_date']}")
        print("-" * 50)


def main():
    """Main function to parse arguments and process the data."""
    parser = argparse.ArgumentParser(description='Process LongMemEval data')
    parser.add_argument('--filename', type=str, default='data/longmemeval_s.json',
                        help='Path to the JSON file (default: data/longmemeval_s.json)')

    args = parser.parse_args()

    # Ensure the file exists
    if not os.path.exists(args.filename):
        print(f"Error: File '{args.filename}' not found.")
        return

    # Read and process the data
    data = read_data(args.filename)
    print(f"Found {len(data)} questions in the file.")
    print_questions(data)


if __name__ == "__main__":
    main()
