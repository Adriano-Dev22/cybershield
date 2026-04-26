# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅ Yes    |

## Reporting a Vulnerability

If you discover a security vulnerability in CyberShield, please do NOT
open a public issue. Instead, follow these steps:

1. Go to the repository on GitHub
2. Click on "Security" tab
3. Click "Report a vulnerability"
4. Provide a detailed description including:
   - Type of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

You can expect a response within 48 hours.

## Security Best Practices for Contributors

- Never commit secrets, API keys or passwords
- Always use environment variables via .env file
- Keep dependencies up to date
- Follow OWASP guidelines for web security
- Use parameterized queries to prevent SQL injection
- Validate and sanitize all user inputs

## Scope

The following are in scope for vulnerability reports:
- Authentication and authorization bypass
- SQL injection
- Cross-site scripting (XSS)
- Remote code execution
- Sensitive data exposure
- Broken access control
