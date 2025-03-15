#!/usr/bin/env python3
"""
Generate requirements.txt using pip freeze with no maintenance required.
"""

import subprocess
import sys

# Run pip freeze and write directly to requirements.txt
subprocess.run(
    [sys.executable, "-m", "pip", "freeze"],
    stdout=open("requirements.txt", "w"),
    check=True
)

print("Generated requirements.txt successfully") 