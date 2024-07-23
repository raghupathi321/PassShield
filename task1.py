import requests
import hashlib
import re
import string
import random


def check_password_strength(password):
    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[!@#$%^&*|()?{}~:]", password) is None
    password_ok = not (
        length_error
        or digit_error
        or uppercase_error
        or lowercase_error
        or symbol_error
    )

    errors = {
        "length_error": length_error,
        "digit_error": digit_error,
        "uppercase_error": uppercase_error,
        "lowercase_error": lowercase_error,
        "symbol_error": symbol_error,
    }

    return password_ok, errors


def check_pwned_password(password):
    sha1password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    url = f"https://api.pwnedpasswords.com/range/{first5_char}"
    response = requests.get(url)
    hashes = (line.split(":") for line in response.text.splitlines())
    count = next((int(count) for h, count in hashes if h == tail), 0)
    return count


def generate_strong_password(length):
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    digits = string.digits
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    symbols = "@!#$%^&*|()<>?/}{~:"
    password = [
        random.choice(digits),
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(symbols),
    ]
    all_characters = digits + lowercase + uppercase + symbols
    password += random.choices(all_characters, k=length - 4)
    random.shuffle(password)
    return "".join(password)


print(
    r"""
██████╗  █████╗ ███████╗███████╗███████╗██╗  ██╗██╗███████╗██╗     ██████╗ 
██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗
██████╔╝███████║███████╗███████╗███████╗███████║██║█████╗  ██║     ██║  ██║
██╔═══╝ ██╔══██║╚════██║╚════██║╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║
██║     ██║  ██║███████║███████║███████║██║  ██║██║███████╗███████╗██████╔╝
      """
)

print("                                                          made by Raghupathi.A")


def main():
    while True:
        print("\nChoose an option:")
        print("1. Check password strength")
        print("2. Check if password has been leaked")
        print("3. Generate a strong password")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            password = input("Enter the password to check its strength: ")
            password_ok, errors = check_password_strength(password)
            if password_ok:
                print("Password is strong.")
            else:
                print("Password is weak. Errors:")
                print(errors)

        elif choice == "2":
            password = input("Enter the password to check if it has been leaked: ")
            count = check_pwned_password(password)
            if count:
                print(f"Password found in {count} leaks.")
            else:
                print("Password not found in leaks.")

        elif choice == "3":
            length = int(input("Enter the length of the password to generate: "))
            try:
                strong_password = generate_strong_password(length)
                print(f"Generated strong password: {strong_password}")
            except ValueError as e:
                print(e)

        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
