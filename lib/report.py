import os
import subprocess

REPORT_DIR = os.path.expanduser("~/HashHunter/reports")
os.makedirs(REPORT_DIR, exist_ok=True)

def generate_report(prepared_file, output_file):
    try:
        print(f"[+] Generating report from cracked hashes...")

        # Run John to show cracked passwords
        result = subprocess.run(
            ["john", "--show", "--format=nt", prepared_file],
            capture_output=True, text=True, check=True
        )

        lines = result.stdout.strip().split('\n')

        # Redirect output path to reports directory
        report_path = os.path.join(REPORT_DIR, os.path.basename(output_file))

        with open(report_path, 'w') as report:
            report.write("=== HashHunter Cracked Password Report ===\n\n")
            for line in lines:
                if ':' in line and '$NT$' not in line and not line.startswith(('Loaded ', 'password hashes', 'Session')):
                    user, password = line.split(':', 1)
                    report.write(f"[+] {user.strip()}: {password.strip()}\n")

        print(f"[+] Report saved to {report_path}")

    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to run john --show: {e}")
    except Exception as e:
        print(f"[!] Failed to generate report: {e}")
