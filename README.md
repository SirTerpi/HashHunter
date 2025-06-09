# 🔐 HashHunter

**HashHunter** is a Python-based offensive security tool designed to **extract**, **crack**, and **report on NTLM password hashes** from Windows systems. It automates common post-exploitation tasks using `secretsdump.py` (Impacket) and `John the Ripper`, supporting both local and remote targets.

---

## 🚀 Features

- Extracts NTLM hashes from:
  - Remote Windows hosts via SMB
  - Local SAM & SYSTEM registry hive files
  - Pre-dumped hash files
- Cracks NTLM hashes using dictionary attacks (wordlists)
- Outputs clean cracked credential reports
- Modular design: `extract`, `crack`, and `report` modules

---

## 📦 Dependencies

Before using HashHunter, make sure the following are installed in your Python environment (ideally within a `venv`):

### 🐍 Python Packages:
- Python 3.8+  
- [Impacket](https://github.com/fortra/impacket) (cloned and installed locally)
- `john` (John the Ripper must be installed on your system)(Note that default versions of john pre-installed on linux may not have NTLM formatting available)

### ✅ Setup (from WSL or Linux/macOS)

```bash
# Create project folder and clone Impacket
cd ~/HashHunter
python3 -m venv venv
source venv/bin/activate

# Clone and install impacket
mkdir lib
cd lib
git clone https://github.com/fortra/impacket.git
cd impacket
pip install .
