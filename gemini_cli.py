#!/usr/bin/env python3
"""
gemini_cli.py - CLI for agents to access Gemini thinking and research models.

Usage:
    python gemini_cli.py think "your prompt"
    python gemini_cli.py think --show-thinking "your prompt"
    python gemini_cli.py research "your research query"
    echo "prompt" | python gemini_cli.py think

Exit codes: 0=success, 1=API error, 2=timeout, 3=unexpected state, 4=config error
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- Model IDs (update here when Google releases new versions) ---
THINK_MODEL = "gemini-3-pro-preview"
RESEARCH_MODEL = "deep-research-pro-preview-12-2025"

# --- Token logging ---
TOKEN_LOG = Path(__file__).parent / "token_usage.jsonl"


def log_tokens(command: str, model: str, usage_metadata, prompt_chars: int) -> None:
    """Append token usage to token_usage.jsonl and print summary to stderr."""
    if not usage_metadata:
        return
    input_tok = getattr(usage_metadata, "prompt_token_count", 0) or 0
    output_tok = getattr(usage_metadata, "candidates_token_count", 0) or 0
    thinking_tok = getattr(usage_metadata, "thoughts_token_count", 0) or 0
    total_tok = getattr(usage_metadata, "total_token_count", 0) or input_tok + output_tok
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": "gemini",
        "model": model,
        "command": command,
        "input_tokens": input_tok,
        "output_tokens": output_tok,
        "thinking_tokens": thinking_tok,
        "total_tokens": total_tok,
        "prompt_chars": prompt_chars,
    }
    try:
        with open(TOKEN_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass
    print(f"[tokens] gemini {command}: {input_tok} in / {output_tok} out / {thinking_tok} thinking / {total_tok} total", file=sys.stderr)


def get_api_key() -> str:
    """Load API key from environment or .env file. Fails explicitly if missing."""
    load_dotenv()
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("ERROR: GEMINI_API_KEY not found.", file=sys.stderr)
        print("Set it in .env file or as an environment variable.", file=sys.stderr)
        print("Expected .env format:", file=sys.stderr)
        print("  GEMINI_API_KEY=your_key_here", file=sys.stderr)
        sys.exit(4)
    return key


def create_client(api_key: str) -> genai.Client:
    """Create and return a Gemini API client."""
    return genai.Client(api_key=api_key)


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
    print('  python gemini_cli.py think "your prompt here"', file=sys.stderr)
    print('  echo "your prompt" | python gemini_cli.py think', file=sys.stderr)
    sys.exit(4)


def run_think(
    client: genai.Client, prompt: str, show_thinking: bool, thinking_level: str
) -> None:
    """Send prompt to Gemini 3 Pro with thinking. Print response to stdout."""
    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level=thinking_level,
            include_thoughts=show_thinking,
        )
    )

    print(f"[think] Model: {THINK_MODEL}", file=sys.stderr)
    print(f"[think] Thinking level: {thinking_level}", file=sys.stderr)
    print(f"[think] Sending prompt ({len(prompt)} chars)...", file=sys.stderr)

    try:
        response = client.models.generate_content(
            model=THINK_MODEL,
            contents=prompt,
            config=config,
        )
    except Exception as e:
        print(f"ERROR: Gemini API call failed: {e}", file=sys.stderr)
        sys.exit(1)

    if not response.candidates:
        print("ERROR: No response candidates returned.", file=sys.stderr)
        sys.exit(1)

    log_tokens("think", THINK_MODEL, getattr(response, "usage_metadata", None), len(prompt))

    if show_thinking:
        for part in response.candidates[0].content.parts:
            if hasattr(part, "thought") and part.thought:
                print("--- THINKING ---")
                print(part.text)
                print("--- END THINKING ---")
                print()
            else:
                print("--- RESPONSE ---")
                print(part.text)
    else:
        print(response.text)


def auto_output_path(prompt: str) -> str:
    """Generate a timestamped output filename from the prompt."""
    slug = re.sub(r"[^a-z0-9]+", "_", prompt[:50].lower()).strip("_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"outputs/{timestamp}_{slug}.md"


def run_research(
    client: genai.Client,
    prompt: str,
    output_path: str,
    poll_interval: int,
    timeout: int,
) -> None:
    """Start deep research, poll until complete, save report and print to stdout."""
    print(f"[research] Model: {RESEARCH_MODEL}", file=sys.stderr)
    print(f"[research] Sending research query ({len(prompt)} chars)...", file=sys.stderr)

    try:
        interaction = client.interactions.create(
            input=prompt,
            agent=RESEARCH_MODEL,
            background=True,
        )
    except Exception as e:
        print(f"ERROR: Failed to start research interaction: {e}", file=sys.stderr)
        sys.exit(1)

    interaction_id = interaction.id
    print(f"[research] Started interaction: {interaction_id}", file=sys.stderr)
    print(
        f"[research] Polling every {poll_interval}s (timeout: {timeout}s)",
        file=sys.stderr,
    )

    start_time = time.time()

    while True:
        elapsed = time.time() - start_time

        if elapsed > timeout:
            print(
                f"[research] TIMEOUT after {elapsed:.0f}s. "
                f"Interaction {interaction_id} may still be running on Google's servers.",
                file=sys.stderr,
            )
            sys.exit(2)

        try:
            interaction = client.interactions.get(interaction_id)
        except Exception as e:
            print(
                f"[research] WARNING: Poll failed ({e}), retrying in {poll_interval}s...",
                file=sys.stderr,
            )
            time.sleep(poll_interval)
            continue

        status = interaction.status
        print(
            f"[research] Status: {status} (elapsed: {elapsed:.0f}s)", file=sys.stderr
        )

        if status == "completed":
            report_text = interaction.outputs[-1].text

            usage_metadata = getattr(interaction, "usage_metadata", None)
            log_tokens("research", RESEARCH_MODEL, usage_metadata, len(prompt))

            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(report_text, encoding="utf-8")

            print(f"[research] Saved to: {output_path}", file=sys.stderr)
            print(report_text)
            return

        elif status == "failed":
            error_info = getattr(interaction, "error", "unknown error")
            print(f"[research] FAILED: {error_info}", file=sys.stderr)
            sys.exit(1)

        elif status == "cancelled":
            print("[research] CANCELLED by server.", file=sys.stderr)
            sys.exit(1)

        elif status in ("in_progress", "requires_action"):
            time.sleep(poll_interval)

        else:
            print(
                f"[research] UNEXPECTED STATUS: '{status}'. "
                f"This is a bug or API change. Aborting.",
                file=sys.stderr,
            )
            sys.exit(3)


def build_parser() -> argparse.ArgumentParser:
    """Build CLI argument parser with think/research subcommands."""
    parser = argparse.ArgumentParser(
        description="CLI for agents to access Gemini thinking and research models.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            '  python gemini_cli.py think "Explain the ELBO"\n'
            '  python gemini_cli.py think --show-thinking "Why does VI underestimate variance?"\n'
            '  python gemini_cli.py research "Survey probabilistic circuits 2025-2026"\n'
            '  echo "prompt" | python gemini_cli.py think\n'
        ),
    )
    subparsers = parser.add_subparsers(dest="command")

    think_parser = subparsers.add_parser(
        "think", help="Gemini 3 Pro with thinking/reasoning"
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
        help="Thinking depth (default: high)",
    )

    research_parser = subparsers.add_parser(
        "research", help="Gemini Deep Research agent (async, saves to file)"
    )
    research_parser.add_argument("prompt", nargs="?", default=None, help="The research query")
    research_parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: auto-generated in outputs/)",
    )
    research_parser.add_argument(
        "--poll-interval",
        type=int,
        default=10,
        help="Seconds between status checks (default: 10)",
    )
    research_parser.add_argument(
        "--timeout",
        type=int,
        default=3600,
        help="Max seconds to wait (default: 3600)",
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
        run_think(client, prompt, args.show_thinking, args.thinking_level)
    elif args.command == "research":
        output = args.output or auto_output_path(prompt)
        run_research(client, prompt, output, args.poll_interval, args.timeout)


if __name__ == "__main__":
    main()
