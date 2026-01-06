# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

"""
ZQAutoNXG - Next-Generation eXtended Automation Platform
Powered by ZQ AI LOGIC™

Copyright © 2025 Zubin Qayam — All Rights Reserved
Licensed under the Apache License, Version 2.0
"""

import logging
import sys

__title__ = "ZQAutoNXG"
__version__ = "6.0.0"
__architecture__ = "G V2 NovaBase"
__brand__ = "Powered by ZQ AI LOGIC™"
__description__ = "Next-Generation eXtended Automation Platform"
__copyright__ = "© 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC"
__license__ = "Apache License 2.0"
__author__ = "Zubin Qayam"
__email__ = "zubin.qayam@outlook.com"

__all__ = [
    "__title__",
    "__version__",
    "__architecture__",
    "__brand__",
    "__description__",
    "__copyright__",
    "__license__",
    "__author__",
    "__email__"
]

# Version validation

# Initialize logging
logging.getLogger("zqautonxg").addHandler(logging.NullHandler())

# ZQAutoNXG startup banner
def _startup_banner() -> None:
    """Display ZQAutoNXG startup information"""
    banner = f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                        ZQAutoNXG                              ║
    ║          Next-Generation eXtended Automation Platform         ║
    ║                   Powered by ZQ AI LOGIC™                     ║
    ║                                                              ║
    ║  Version: {__version__:<20} Architecture: {__architecture__:<15} ║
    ║  License: Apache License 2.0                                 ║
    ║  Copyright © 2025 Zubin Qayam — All Rights Reserved          ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

# Display banner when imported
if __name__ != "__main__":
    _startup_banner()
