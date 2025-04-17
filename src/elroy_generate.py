#!/usr/bin/env python3
"""
Script to generate data for LongMemEval.
This script reads a JSON file and processes the questions.
"""

import json
import argparse
import os
import csv
import sys
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


def filter_questions(data, question_type=None, limit=None):
    """
    Filter questions based on criteria.

    Args:
        data (list): List of question entries
        question_type (str, optional): Filter by question type
        limit (int, optional): Limit the number of questions

    Returns:
        list: Filtered list of question entries
    """
    filtered_data = data

    # Filter by question type if specified
    if question_type:
        filtered_data = [entry for entry in filtered_data
                         if entry['question_type'] == question_type]

    # Limit the number of questions if specified
    if limit and limit > 0:
        filtered_data = filtered_data[:limit]

    return filtered_data


def print_questions(data, output_format='text', output_file=None):
    """
    Print each question from the data.

    Args:
        data (list): List of question entries
        output_format (str): Output format ('text' or 'csv')
        output_file (str, optional): Path to output file for CSV format
    """
    if output_format == 'text':
        for i, entry in enumerate(data):
            print(f"Question {i+1} (ID: {entry['question_id']}):")
            print(f"Type: {entry['question_type']}")
            print(f"Question: {entry['question']}")
            print(f"Answer: {entry['answer']}")
            print(f"Date: {entry['question_date']}")
            print("-" * 50)

    elif output_format == 'csv':
        fieldnames = ['question_id', 'question_type', 'question', 'answer', 'question_date']

        if output_file:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for entry in data:
                    writer.writerow({field: entry[field] for field in fieldnames})
            print(f"CSV output written to {output_file}")
        else:
            writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
            writer.writeheader()
            for entry in data:
                writer.writerow({field: entry[field] for field in fieldnames})


def main():
    """Main function to parse arguments and process the data."""
    parser = argparse.ArgumentParser(description='Process LongMemEval data')
    parser.add_argument('--filename', type=str, default='data/longmemeval_s.json',
                        help='Path to the JSON file (default: data/longmemeval_s.json)')
    parser.add_argument('--type', type=str,
                        help='Filter by question type (e.g., single-session-user)')
    parser.add_argument('--limit', type=int,
                        help='Limit the number of questions displayed')
    parser.add_argument('--format', type=str, choices=['text', 'csv'], default='text',
                        help='Output format (text or csv)')
    parser.add_argument('--output', type=str,
                        help='Output file for CSV format')

    args = parser.parse_args()

    # Ensure the file exists
    if not os.path.exists(args.filename):
        print(f"Error: File '{args.filename}' not found.")
        return

    # Read the data
    data = read_data(args.filename)
    print(f"Found {len(data)} questions in the file.")

    # Filter the data
    filtered_data = filter_questions(data, args.type, args.limit)
    print(f"Displaying {len(filtered_data)} questions after filtering.")

    # Print the questions
    print_questions(filtered_data, args.format, args.output)


if __name__ == "__main__":
    main()
