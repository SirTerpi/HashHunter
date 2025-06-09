import subprocess
import os
import sys

def prepare_john_file(input_file, output_file):
    print(f"[+] Preparing {output_file}...")

    valid_lines = 0
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()

            if not line or line.startswith('[') or 'Impacket' in line or 'bootKey' in line or 'Cleaning up' in line:
                continue

            parts = line.split(':')
            if len(parts) >= 4:
                username = parts[0]
                nt_hash = parts[3]

                if nt_hash and nt_hash != 'aad3b435b51404eeaad3b435b51404ee':
                    outfile.write(f"{username}:$NT${nt_hash}\n")
                    print(f"[+] Added: {username}:$NT${nt_hash}")
                    valid_lines += 1

    if valid_lines == 0:
        print("[!] No valid NT hashes found to write to john_ready.txt.")

def crack_hashes_john(hash_file, wordlist_filename):
    try:
        print(f"[+] Preprocessing {hash_file} for John format...")

        prepared_file = os.path.abspath("john_ready.txt")

        # Build path to wordlist within ~/HashHunter/wordlists/
        wordlist_path = os.path.abspath(os.path.join("wordlists", wordlist_filename))

        # Check if wordlist exists
        if not os.path.isfile(wordlist_path):
            print(f"[!] Wordlist file not found: {wordlist_path}")
            sys.exit(1)

        prepare_john_file(hash_file, prepared_file)

        print(f"[+] Cracking hashes in {prepared_file} using {wordlist_path}...")

        subprocess.run([
            "john",
            "--format=nt",
            f"--wordlist={wordlist_path}",
            prepared_file
        ], check=True)

        print("[+] Cracked password results:")
        subprocess.run([
            "john",
            "--show",
            "--format=nt",
            prepared_file
        ], check=True)

    except subprocess.CalledProcessError as e:
        print(f"[!] Cracking failed: {e}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
