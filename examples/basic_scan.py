from hexforge_lite.engine import ScanEngine

report = ScanEngine().scan("https://example.com")
print(report["summary"])
