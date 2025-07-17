#!/usr/bin/env python3
"""
Run script for AI Notes Summarizer
"""

import subprocess
import sys
import os


def main():
    """Run the Streamlit application"""
    try:
        # Change to the application directory
        app_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(app_dir)

        # Run streamlit
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "app.py",
                "--server.headless",
                "true",
                "--server.port",
                "8501",
                "--server.address",
                "0.0.0.0",
            ]
        )
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Error running application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
