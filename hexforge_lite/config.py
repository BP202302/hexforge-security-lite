import os
from pathlib import Path

VERSION = "1.7.0-community"
PORT = int(os.environ.get("PORT", "8000"))
MAX_URLS_PER_SESSION = 50
REQUEST_TIMEOUT = 12
ROBOTS_TIMEOUT = 5
MAX_BODY_BYTES = 600_000
USER_AGENT = f"HexForgeSecurityLite/{VERSION}"
BASE_DIR = Path(__file__).resolve().parent.parent
SITE_URL = "https://hexforgeai.dev"
PAYPAL_URL = "https://www.paypal.com/donate/?hosted_button_id=S3335NNBYZXES"
AUTHOR_NAME = "Brandon Steven Barrera Portillo"
AUTHOR_EMAIL = "brandonstevenbarrera@gmail.com"
GITHUB_URL = "https://github.com/BP202302/hexforge-security-lite"
TRADEMARK_NOTICE = (
    "HexForge Security, the HexForge name, logo, and brand assets are reserved. "
    "Commercial use, rebranding, and SaaS resale require written permission."
)
