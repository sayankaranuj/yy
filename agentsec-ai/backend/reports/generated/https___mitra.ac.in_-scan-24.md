# AgentSec AI Report for https://mitra.ac.in/

## Summary
- Target: https://mitra.ac.in/
- Scan ID: 24
- Findings: 1

## Findings
- Microsoft Azure Domain Tenant ID - Detect [info]
  - Location: https://login.microsoftonline.com:443/mitra.ac.in/v2.0/.well-known/openid-configuration
  - Evidence: "curl -X 'GET' -d '' -H 'Host: login.microsoftonline.com' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0' 'https://login.microsoftonline.com:443/mitra.ac.in/v2.0/.well-known/openid-configuration'"