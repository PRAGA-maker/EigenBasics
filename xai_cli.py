#!/usr/bin/env python3
"""
xai_cli.py - CLI for agents to access xAI Grok reasoning and search models.

Usage:
    python xai_cli.py think "your prompt"
    python xai_cli.py think --show-thinking "your prompt"
    python xai_cli.py research "your research query"
    echo "prompt" | python xai_cli.py think

Exit codes: 0=success, 1=API error, 2=timeout, 3=unexpected state, 4=config error
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# --- Model ID ---
MODEL = "grok-4-1-fast-reasoning"


def get_api_key() -> str:
    """Load API key from environment or .env file. Fails explicitly if missing."""
    load_dotenv()
    key = os.environ.get("XAI_API_KEY")
    if not key:
        print("ERROR: XAI_API_KEY not found.", file=sys.stderr)
        print("Set it in .env file or as an environment variable.", file=sys.stderr)
        print("Expected .env format:", file=sys.stderr)
        print("  XAI_API_KEY=your_key_here", file=sys.stderr)
        sys.exit(4)
    return key


def create_client(api_key: str) -> OpenAI:
    """Create and return an xAI API client (OpenAI-compatible)."""
    return OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")


def get_prompt(args_prompt: str | None) -> str:
    """Get prompt from CLI arg or stdin. Fails explicitly if neither provides input."""
    if args_prompt:
        return args_prompt

    if not sys.stdin.isatty():
        prompt = sys.stdin.read().strip()
        if prompt:
            return prompt

    print("ERROR: No prompt provided.", file=sys.stderr)
    print("Provide a prompt as an argument or pipe via stdin.", file=sys.stderr)
    print('  python xai_cli.py think "your prompt here"', file=sys.stderr)
    print('  echo "your prompt" | python xai_cli.py think', file=sys.stderr)
    sys.exit(4)


def run_think(client: OpenAI, prompt: str, show_thinking: bool) -> None:
    """Send prompt to Grok reasoning model. Print response to stdout."""
    print(f"[think] Model: {MODEL}", file=sys.stderr)
    print(f"[think] Sending prompt ({len(prompt)} chars)...", file=sys.stderr)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        print(f"ERROR: xAI API call failed: {e}", file=sys.stderr)
        sys.exit(1)

    if not response.choices:
        print("ERROR: No response choices returned.", file=sys.stderr)
        sys.exit(1)

    message = response.choices[0].message

    if show_thinking:
        reasoning_tokens = 0
        if response.usage and hasattr(response.usage, "completion_tokens_details"):
            details = response.usage.completion_tokens_details
            reasoning_tokens = getattr(details, "reasoning_tokens", 0) or 0
        print(f"[think] Reasoning tokens used: {reasoning_tokens}", file=sys.stderr)
        print("--- RESPONSE ---")

    print(message.content)


def auto_output_path(prompt: str) -> str:
    """Generate a timestamped output filename from the prompt."""
    slug = re.sub(r"[^a-z0-9]+", "_", prompt[:50].lower()).strip("_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"outputs/{timestamp}_{slug}.md"


def run_research(client: OpenAI, prompt: str, output_path: str) -> None:
    """Send research query to Grok with web search via Responses API. Save report and print to stdout."""
    print(f"[research] Model: {MODEL}", file=sys.stderr)
    print(f"[research] Web search: enabled (Responses API)", file=sys.stderr)
    print(f"[research] Sending research query ({len(prompt)} chars)...", file=sys.stderr)

    try:
        response = client.responses.create(
            model=MODEL,
            instructions=(
                "You are a research assistant with web search capabilities. "
                "Search the web thoroughly to answer the user's research query. "
                "Provide a comprehensive, well-sourced response with citations where possible."
            ),
            input=prompt,
            tools=[{"type": "web_search"}],
        )
    except Exception as e:
        print(f"ERROR: xAI API call failed: {e}", file=sys.stderr)
        sys.exit(1)

    report_text = response.output_text
    if not report_text:
        print("ERROR: Empty response from model.", file=sys.stderr)
        sys.exit(1)

    if response.usage:
        usage = response.usage
        details = getattr(usage, "model_extra", {}) or {}
        searches = details.get("num_server_side_tools_used", 0)
        print(f"[research] Web searches performed: {searches}", file=sys.stderr)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report_text, encoding="utf-8")

    print(f"[research] Saved to: {output_path}", file=sys.stderr)
    print(report_text)


def build_parser() -> argparse.ArgumentParser:
    """Build CLI argument parser with think/research subcommands."""
    parser = argparse.ArgumentParser(
        description="CLI for agents to access xAI Grok reasoning and search models.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            '  python xai_cli.py think "Explain the ELBO"\n'
            '  python xai_cli.py think --show-thinking "Why does VI underestimate variance?"\n'
            '  python xai_cli.py research "Survey probabilistic circuits 2025-2026"\n'
            '  echo "prompt" | python xai_cli.py think\n'
        ),
    )
    subparsers = parser.add_subparsers(dest="command")

    think_parser = subparsers.add_parser(
        "think", help="Grok reasoning model with thinking/reasoning"
    )
    think_parser.add_argument("prompt", nargs="?", default=None, help="The prompt")
    think_parser.add_argument(
        "--show-thinking",
        action="store_true",
        help="Include the model's reasoning process in output",
    )
    think_parser.add_argument(
        "--thinking-level",
        choices=["low", "high"],
        default="high",
        help="Reasoning effort (default: high)",
    )

    research_parser = subparsers.add_parser(
        "research", help="Grok with web search (saves to file)"
    )
    research_parser.add_argument("prompt", nargs="?", default=None, help="The research query")
    research_parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: auto-generated in outputs/)",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(4)

    api_key = get_api_key()
    client = create_client(api_key)
    prompt = get_prompt(getattr(args, "prompt", None))

    if args.command == "think":
        run_think(client, prompt, args.show_thinking)
    elif args.command == "research":
        output = args.output or auto_output_path(prompt)
        run_research(client, prompt, output)


if __name__ == "__main__":
    main()
