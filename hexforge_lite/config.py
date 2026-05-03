import os
from pathlib import Path

VERSION = "1.9.0-stable"
PORT = int(os.environ.get("PORT", "8000"))
MAX_URLS_PER_SESSION = 50
REQUEST_TIMEOUT = 12
ROBOTS_TIMEOUT = 5
MAX_BODY_BYTES = 600_000
FETCH_TEXT_MAX_BYTES = 100_000
JS_FETCH_MAX_BYTES = 350_000
MAX_API_BODY_BYTES = 8192
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_SCANS = 20
ENABLE_PLUGINS = os.environ.get("HEXFORGE_ENABLE_PLUGINS", "1") not in {"0", "false", "False"}
ENABLE_LITE_ACTIVE_CHECKS = os.environ.get("HEXFORGE_ENABLE_LITE_ACTIVE", "1") not in {"0", "false", "False"}
LITE_ACTIVE_TIMEOUT = 5
USER_AGENT = f"HexForgeSecurityLite/{VERSION}"
BASE_DIR = Path(__file__).parent.parent
SITE_URL = "https://hexforgeai.dev/"
PAYPAL_URL = "https://www.paypal.com/donate/?hosted_button_id=S3335NNBYZXES"
AUTHOR_NAME = "Brandon Steven Barrera Portillo"
AUTHOR_EMAIL = "brandonstevenbarrera@gmail.com"
GITHUB_URL = "https://github.com/BP202302/hexforge-security-lite"
TRADEMARK_NOTICE = (
    "HexForge Security, the HexForge name, logo, and brand assets are reserved. "
    "Commercial use, rebranding, and SaaS resale require written permission."
)

DEMO_URL = "https://hexforge-security-lite.onrender.com"
ENABLE_DEMO_WAITLIST = os.environ.get("HEXFORGE_ENABLE_WAITLIST", "1") not in {"0", "false", "False"}
WAITLIST_FILE = BASE_DIR / "data" / "pro_waitlist.jsonl"
