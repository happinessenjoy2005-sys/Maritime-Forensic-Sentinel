# 🦈 Guardian V6: Maritime Forensic Sentinel

## 🌊 Overview
Guardian V6 is a Python-based forensic file monitor designed to detect unauthorized image files in sensitive directories. It was built with a specific focus on maritime security and anti-poaching efforts, simulating a "National Park" patrol environment.

## 🛡️ Key Features
*   **Real-time Monitoring:** Uses the OS to track file movements instantly.
*   **Forensic Integrity:** Generates SHA-256 hashes (digital fingerprints) for every detected file to ensure the chain of custody.
*   **Metadata Extraction:** Automatically pulls GPS coordinates from EXIF data to map the location of the "incident."
*   **Telegram Integration:** Sends instant "ARRESTED!" alerts with a direct Google Maps link to the response team's mobile device.

## 🛠️ Tech Stack
*   **Language:** Python 3
*   **Libraries:** `requests`, `Pillow` (for EXIF processing), `hashlib`
*   **Security:** Uses `.env` for API token management to prevent credential leakage.

## 🇦🇺 About the Developer
Currently a University student specializing in **Cybersecurity**, I developed this project as part of my portfolio for future roles in **Threat Hunting** and **Maritime Digital Forensics**.
