#!/usr/bin/python3
# File name          : protintel.py
# Original Author    : @C3n7ral051nt4g3ncy
# This fork by       : be0vlk

import requests
import re
import datetime
import sys
import openpyxl
import os


def banner():
    print(
        """\033[1;32m
* * * * * * * * * * * * * * * * * * * *
*  ___         _   _ _  _ _____    _  *
* | _ \_ _ ___| |_/ | \| |_   _|__| | *
* |  _/ '_/ _ \  _| | .` | | |/ -_) | *
* |_| |_| \___/\__|_|_|\_| |_|\___|_| *
*                                     *
* * * * * * * * * * * * * * * * * * * *                                                                     

Original GitHub:  https://github.com/C3n7ral051nt4g3ncy                                                          
Fork by be0vlk:   https://github.com/be0vlk/Protintel
_______________________________________________________\033[0m                                                                                                                                       
"""
    )


def extract_timestamp(source_code):
    timestamp = re.findall(r":(\d{10}):", source_code)
    return int(timestamp[0]) if timestamp else None


def extract_key_and_length(source_code):
    key_line = source_code.split("\n")[1]
    key_parts = key_line.split(":")
    try:
        key_type = key_parts[2]
        key_length = key_parts[3]
    except IndexError:
        key_type = key_length = None
    return key_type, key_length


def check_email(email):
    print(f"\n\033[1;34mChecking email: {email}\033[0m")
    url = f"https://api.protonmail.ch/pks/lookup?op=index&search={email}"
    response = requests.get(url)
    if response.text.startswith("info:1:1"):
        email_domain = email.split("@")[1]
        if email_domain in ["protonmail.com", "protonmail.ch", "proton.me"]:
            print("\033[1;32mThis is a Protonmail address.\033[0m")
        else:
            print("\033[1;32mThis is a Protonmail custom domain.\033[0m")
        data = response.text.split("\n")
        uid_line = data[2]
        email_in_brackets = re.findall(r"<(.*?)>", uid_line)
        if email_in_brackets:
            actual_email = email_in_brackets[0]
            if actual_email != email:
                print(
                    "\033[1;33mCatch-All detected, this is the main email -->\033[0m",
                    actual_email,
                )
        timestamp = extract_timestamp(response.text)
        if timestamp is not None:
            creation_date = datetime.datetime.fromtimestamp(
                timestamp, datetime.timezone.utc
            ).strftime("%Y-%m-%d %H:%M:%S")
            print("\033[1;32mPGP Key Date and Creation Time:\033[0m", creation_date)
        else:
            print("\033[1;31mProblem parsing Key Creation Date.\033[0m")
        key_type, key_length = extract_key_and_length(response.text)
        if key_type is not None:
            if key_type != "22":
                print(f"\033[1;32mEncryption Standard : RSA {key_length}-bit\033[0m")
            else:
                print("\033[1;32mEncryption Standard : ECC Curve25519\033[0m")
        else:
            print("\033[1;31mProblem parsing Encryption Standard.\033[0m")
    else:
        print("\033[1;31mNot a Protonmail custom domain\033[0m")


def extract_emails_from_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    target_emails = []

    if file_extension == ".xlsx":
        try:
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active
            for row in sheet.iter_rows():
                for cell in row:
                    if re.match(
                        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                        str(cell.value),
                    ):
                        target_emails.append(str(cell.value))
        except:
            print(f"\033[1;31mError reading xlsx file: {file_path}\033[0m")
    else:
        try:
            with open(file_path, "r") as file:
                target_emails = re.findall(
                    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", file.read()
                )
        except:
            print(f"\033[1;31mError reading file: {file_path}\033[0m")

    return target_emails


if __name__ == "__main__":
    banner()
    if len(sys.argv) < 2:
        print(
            "\033[1;31mPlease provide at least one email address or file path as an argument.\033[0m"
        )
        sys.exit(1)

    emails = []

    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            emails.extend(extract_emails_from_file(arg))
        elif re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", arg):
            emails.append(arg)
        else:
            print(f"\033[1;31mInvalid argument: {arg}\033[0m")

    if not emails:
        print("\033[1;31mNo valid email addresses found.\033[0m")
        sys.exit(1)

    for email in emails:
        check_email(email)
