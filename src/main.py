#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sketch-of-Thought AI Agent: Main Entry Point

This script initializes and runs the Sketch-of-Thought AI Agent,
which combines real-time environmental awareness with efficient reasoning.
"""

import os
import argparse
import logging
from dotenv import load_dotenv

from agent.core import SoTAgent

# Load environment variables
load_dotenv()

# Setup logging
logging_level = os.getenv("LOG_LEVEL", "info").upper()
logging_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}
logging.basicConfig(
    level=logging_levels.get(logging_level, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Sketch-of-Thought AI Agent")
    parser.add_argument(
        "--mode",
        type=str,
        default="interactive",
        choices=["interactive", "server", "demo"],
        help="Agent operation mode"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    return parser.parse_args()

def main():
    """
    Main entry point for the SoT AI Agent.
    """
    args = parse_args()
    
    # Override debug setting from environment if specified in args
    debug_mode = args.debug or (os.getenv("DEBUG_MODE", "false").lower() == "true")
    if debug_mode:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
    
    # Initialize the agent
    logger.info("Initializing Sketch-of-Thought AI Agent")
    agent = SoTAgent()
    
    # Run in the specified mode
    if args.mode == "interactive":
        logger.info("Starting interactive mode")
        agent.run_interactive()
    elif args.mode == "server":
        logger.info("Starting server mode")
        agent.run_server()
    elif args.mode == "demo":
        logger.info("Running demo")
        agent.run_demo()

if __name__ == "__main__":
    main()
