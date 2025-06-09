#!/usr/bin/env python3

import argparse
import sys
import os
from lib import extract, crack, report

def main():
    parser = argparse.ArgumentParser(
        prog="HashHunter",
        description="\U0001f575️ HashHunter: Extract and crack password hashes from Windows systems."
    )

    parser.add_argument('--mode', required=True, choices=['remote', 'local', 'hashfile'],
                        help='Choose mode: remote (SMB), local (SAM), or hashfile (pre-dumped).')

    parser.add_argument('--target', help='Target IP address (for remote mode).')
    parser.add_argument('--username', help='Admin username (for remote mode).')
    parser.add_argument('--password', help='Admin password (for remote mode).')

    parser.add_argument('--sam', help='Path to SAM hive file (for local mode).')
    parser.add_argument('--system', help='Path to SYSTEM hive file (for local mode).')

    parser.add_argument('--hashfile', help='Path to a hash file (for hashfile mode).')
    parser.add_argument('--wordlist', default='wordlists/rockyou.txt', help='Wordlist for cracking')
    parser.add_argument('--report', default='cracked_output.txt', help='Report file output path.')

    args = parser.parse_args()

    prepared_file = os.path.abspath("john_ready.txt")

    # Route based on mode
    if args.mode == 'remote':
        if not (args.target and args.username and args.password):
            print("[!] Remote mode requires --target, --username, and --password.")
            sys.exit(1)
        print("[*] Running remote hash extraction...")
        extract.extract_from_remote(args.target, args.username, args.password)
        crack.crack_hashes_john('remote_hashes.txt', args.wordlist)
        report.generate_report(prepared_file, args.report)

    elif args.mode == 'local':
        if not (args.sam and args.system):
            print("[!] Local mode requires --sam and --system file paths.")
            sys.exit(1)
        print("[*] Running local SAM extraction...")
        extract.extract_from_sam_system(args.sam, args.system)
        crack.crack_hashes_john('local_hashes.txt', args.wordlist)
        report.generate_report(prepared_file, args.report)

    elif args.mode == 'hashfile':
        if not args.hashfile:
            print("[!] Hashfile mode requires --hashfile.")
            sys.exit(1)
        print("[*] Cracking provided hash file...")
        crack.crack_hashes_john(args.hashfile, args.wordlist)
        report.generate_report(prepared_file, args.report)

    else:
        print("[!] Invalid mode. Use --help for options.")

if __name__ == '__main__':
    main()
