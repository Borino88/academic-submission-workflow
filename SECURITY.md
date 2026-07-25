# Security Policy & Container Hardening

## 1. Supported Versions
| Version | Supported | Security & Container Status |
| :--- | :---: | :--- |
| **`1.0.x`** | ✅ Yes | Multi-Stage Build, Non-Root Runtime (`UID 1000`), Trivy Verified |

## 2. Reporting a Vulnerability
Please report potential vulnerabilities or security bugs directly to [a.borino88@gmail.com](mailto:a.borino88@gmail.com).

## 3. Container Security Safeguards
* **Non-Root Execution:** The Docker container executes strictly under an unprivileged user (`appuser`, UID `1000`, GID `1000`).
* **Multi-Stage Build:** Compilation dependencies and wheel builders are excluded from the final runtime image.
* **Trivy CI Scanning:** Every push is evaluated by automated vulnerability and secret scanners before publishing to Docker Hub.
