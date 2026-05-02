# Lite Boundaries

HexForge Security Lite is intentionally defensive and conservative.

It may:

- fetch an authorized URL with a normal HTTP request
- inspect response headers and HTML
- check a small number of same-origin static JavaScript files for visible route references
- summarize TLS and public discovery files
- classify findings with evidence, confidence and precision notes

It does not:

- exploit vulnerabilities
- brute force credentials
- fuzz parameters
- bypass authentication
- submit forms
- perform destructive or disruptive tests

The client-surface module is a passive navigation map, not a vulnerability claim. A bounty report still requires separate manual proof of impact.
