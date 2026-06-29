from flask import Flask, render_template, request
from dbConnection import save_password, delete_password
import random

app = Flask(__name__)

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
letters_lower = letters.lower()
digits = "0123456789"
symbols = "!@#$%^&*()_+-=[]{}|;:',.<>?/`~\\ "

def get_min_max_length(password):
    return 8 <= len(password) <= 16

def contains_all_req(password):
    missing = []
    if not get_min_max_length(password):
        missing.append("Password must be 8–16 characters")
    if not any(c in letters for c in password):
        missing.append("Missing Uppercase Letter")

    if not any(c in letters_lower for c in password):
        missing.append("Missing Lowercase Letter")

    if not any(c in digits for c in password):
        missing.append("Mising Number")

    if not any(c in symbols for c in password):
        missing.append("Missing Special Symbol")
    return missing

def suggest_random_password(length=12):
    chars = [
        random.choice(letters),
        random.choice(letters_lower),
        random.choice(digits),
        random.choice(symbols),
    ]
    all_chars = letters + letters_lower + digits + symbols
    for char in range(length - 4):
        chars.append(random.choice(all_chars))
    random.shuffle(chars)
    return "".join(chars)

@app.route("/", methods=["GET", "POST"])
def home():
    password = ""
    confirm_password = ""
    missing = []
    message = ""
    password_mismatch = False
    generated_password = ""

    if request.method == "POST":
        action = request.form.get("action")
        if action == "generate":
            generated_password = suggest_random_password()
            password = generated_password

        elif action == "save":
            password = request.form.get("password", "")
            confirm_password = request.form.get("confirm_password", "")
            if password != confirm_password:
                password_mismatch = True

            else:
                missing = contains_all_req(password)
                if not missing:
                    inserted_id, password_hash = save_password(password)
                    message = "Password saved successfully."

        elif action == "delete":
            password_id = request.form.get("password_id", "")
            if password_id:
                deleted_rows = delete_password(int(password_id))
                message = "Deleted successfully" if deleted_rows > 0 else "ID not found"
            else:
                message = "Enter ID"

    return render_template(
        "index.html",
        password=password,
        confirm_password=confirm_password,
        missing=missing,
        message=message,
        password_mismatch=password_mismatch,
        generated_password=generated_password
    )


if __name__ == "__main__":
    app.run(debug=True)
