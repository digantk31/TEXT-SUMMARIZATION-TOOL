# python summarizer.py --input_file "C:\Users\digan\Downloads\Intership\CodeTech\Task-1\article.txt"
# python summarizer.py --input_file "…\article.txt" --max_length 100 --min_length 20


#!/usr/bin/env python3
"""
summarizer.py: A command-line tool to summarize lengthy text articles using NLP techniques.

Deliverable for Codtech Internship Task - 1.

Usage:
    python summarizer.py --input_file path/to/article.txt [--model MODEL_NAME] [--max_length N] [--min_length M]

Requirements:
    pip install transformers torch
"""
import argparse
from transformers import pipeline


def load_summarizer(model_name: str = "facebook/bart-large-cnn"):
    """
    Load and return a Hugging Face summarization pipeline.

    :param model_name: Name of the pretrained model to use.
    :return: A transformers.pipeline object for summarization.
    """
    return pipeline("summarization", model=model_name)


def summarize_text(summarizer, text: str, max_length: int = 150, min_length: int = 30) -> str:
    """
    Generate a summary for the given text.

    :param summarizer: The summarization pipeline object.
    :param text: The input text to summarize.
    :param max_length: The upper bound on summary token length.
    :param min_length: The lower bound on summary token length.
    :return: The generated summary string.
    """
    # The pipeline returns a list of dicts; extract the first result's summary_text
    result = summarizer(
        text,
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )
    return result[0]['summary_text']


def main():
    parser = argparse.ArgumentParser(
        description="Summarize input text files using an NLP model."
    )
    parser.add_argument(
        "--input_file",
        type=str,
        required=True,
        help="Path to the input text file to be summarized."
    )
    parser.add_argument(
        "--model",
        type=str,
        default="facebook/bart-large-cnn",
        help="Hugging Face model name for summarization."
    )
    parser.add_argument(
        "--max_length",
        type=int,
        default=150,
        help="Maximum length of the summary in tokens."
    )
    parser.add_argument(
        "--min_length",
        type=int,
        default=30,
        help="Minimum length of the summary in tokens."
    )
    args = parser.parse_args()

    # Read the input article text
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.")
        return

    # Initialize the summarization pipeline
    summarizer = load_summarizer(args.model)

    # Generate and print the summary
    summary = summarize_text(
        summarizer,
        text,
        max_length=args.max_length,
        min_length=args.min_length
    )

    print("\n===== Summary =====\n")
    print(summary)


if __name__ == "__main__":
    main()
