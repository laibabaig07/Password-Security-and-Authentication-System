import tkinter as tk
from tkinter import messagebox, ttk
import hashlib
import string
import math
import random
import re
import pyperclip

# =========================
# DPI FIX FOR WINDOWS
# =========================
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# =========================
# COMMON PASSWORDS
# =========================
COMMON_PASSWORDS = {
    "password", "123456", "123456789", "qwerty", "abc123",
    "password1", "iloveyou", "admin", "letmein", "welcome",
    "monkey", "dragon", "master", "sunshine", "princess",
    "12345678", "1234567", "football", "shadow", "superman",
    "michael", "password123", "pass", "login", "test",
    "hello", "charlie", "donald", "cheese", "batman"
}

# =========================
# PASSWORD FUNCTIONS
# =========================
def calculate_entropy(password):
    pool_size = 0

    if any(c.isupper() for c in password):
        pool_size += 26

    if any(c.islower() for c in password):
        pool_size += 26

    if any(c.isdigit() for c in password):
        pool_size += 10

    if any(not c.isalnum() for c in password):
        pool_size += 32

    if pool_size == 0:
        return 0

    return round(len(password) * math.log2(pool_size), 2)


def estimate_crack_time(entropy):
    guesses = 2 ** entropy
    guesses_per_second = 10_000_000_000

    seconds = guesses / guesses_per_second

    if seconds < 1:
        return "Instantly cracked"

    elif seconds < 60:
        return f"{seconds:.1f} seconds"

    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes"

    elif seconds < 86400:
        return f"{seconds/3600:.1f} hours"

    elif seconds < 31536000:
        return f"{seconds/86400:.1f} days"

    elif seconds < 3.154e9:
        return f"{seconds/31536000:.1f} years"

    else:
        return "Centuries"


def check_patterns(password):
    warnings = []

    if re.search(r'(.)\1{2,}', password):
        warnings.append("⚠ Repeated characters detected")

    if re.search(r'(123|234|345|456|abc|bcd|cde)', password.lower()):
        warnings.append("⚠ Sequential pattern detected")

    if re.search(r'(qwerty|asdf|zxcv)', password.lower()):
        warnings.append("⚠ Keyboard pattern detected")

    if password.lower() in COMMON_PASSWORDS:
        warnings.append("🚨 Common breached password")

    return warnings


def check_strength(password):
    length = len(password)

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    score = 0
    suggestions = []

    criteria = {
        "length": length >= 12,
        "uppercase": has_upper,
        "lowercase": has_lower,
        "digits": has_digit,
        "special": has_special
    }

    if criteria["length"]:
        score += 2
    elif length >= 8:
        score += 1
    else:
        suggestions.append("Use at least 12 characters")

    if has_upper:
        score += 1
    else:
        suggestions.append("Add uppercase letters")

    if has_lower:
        score += 1
    else:
        suggestions.append("Add lowercase letters")

    if has_digit:
        score += 1
    else:
        suggestions.append("Add numbers")

    if has_special:
        score += 2
    else:
        suggestions.append("Add special characters")

    patterns = check_patterns(password)

    if patterns:
        score = max(0, score - len(patterns))

    if score <= 2:
        strength = "Very Weak"
        color = "#e74c3c"

    elif score <= 4:
        strength = "Weak"
        color = "#e67e22"

    elif score <= 5:
        strength = "Moderate"
        color = "#f1c40f"

    elif score <= 6:
        strength = "Strong"
        color = "#2ecc71"

    else:
        strength = "Very Strong"
        color = "#27ae60"

    entropy = calculate_entropy(password)

    return {
        "strength": strength,
        "color": color,
        "score": score,
        "entropy": entropy,
        "crack_time": estimate_crack_time(entropy),
        "suggestions": suggestions,
        "patterns": patterns,
        "criteria": criteria
    }


def generate_hashes(password):
    enc = password.encode()

    return {
        "MD5": hashlib.md5(enc).hexdigest(),
        "SHA-1": hashlib.sha1(enc).hexdigest(),
        "SHA-256": hashlib.sha256(enc).hexdigest(),
        "SHA-512": hashlib.sha512(enc).hexdigest(),
        "BLAKE2b": hashlib.blake2b(enc).hexdigest()
    }


def generate_strong_password(length=20):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="

    while True:
        pwd = ''.join(random.SystemRandom().choice(chars) for _ in range(length))

        if check_strength(pwd)["score"] >= 6:
            return pwd


# =========================
# GUI APP
# =========================
class CipherGuardApp:

    def __init__(self, root):

        self.root = root

        self.root.title("CipherGuard Pro — Password Security Analyzer")

        self.root.geometry("1400x950")
        self.root.minsize(1200, 850)

        self.root.configure(bg="#0d1117")

        root.tk.call('tk', 'scaling', 1.4)

        self.current_hashes = {}

        self.build_ui()

    # =========================
    # UI
    # =========================
    def build_ui(self):

        # HEADER
        header = tk.Frame(self.root, bg="#161b22", pady=20)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🔐 CipherGuard Pro",
            font=("Segoe UI", 34, "bold"),
            bg="#161b22",
            fg="#58a6ff"
        ).pack()

        tk.Label(
            header,
            text="Password Security Analyzer & Hash Generator",
            font=("Segoe UI", 16),
            bg="#161b22",
            fg="#8b949e"
        ).pack()

        # INPUT SECTION
        inp = tk.Frame(self.root, bg="#0d1117", pady=20)
        inp.pack(fill="x", padx=40)

        tk.Label(
            inp,
            text="Enter Password",
            font=("Segoe UI", 18, "bold"),
            bg="#0d1117",
            fg="#c9d1d9"
        ).pack(anchor="w")

        row = tk.Frame(inp, bg="#0d1117")
        row.pack(fill="x", pady=10)

        self.entry = tk.Entry(
            row,
            width=40,
            show="•",
            font=("Segoe UI", 20),
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            relief="solid",
            bd=1
        )

        self.entry.pack(side="left", ipady=10)

        self.entry.bind("<KeyRelease>", lambda e: self.live_update())

        self.show_btn = tk.Button(
            row,
            text="👁",
            command=self.toggle_show,
            bg="#21262d",
            fg="white",
            font=("Segoe UI", 16),
            relief="flat",
            padx=15,
            pady=8
        )

        self.show_btn.pack(side="left", padx=10)

        # STRENGTH LABEL
        self.strength_label = tk.Label(
            inp,
            text="—",
            font=("Segoe UI", 18, "bold"),
            bg="#0d1117",
            fg="#58a6ff"
        )

        self.strength_label.pack(anchor="w", pady=5)

        # BAR
        self.bar_canvas = tk.Canvas(
            inp,
            height=16,
            bg="#21262d",
            highlightthickness=0
        )

        self.bar_canvas.pack(fill="x", pady=10)

        # BUTTONS
        btn_row = tk.Frame(self.root, bg="#0d1117")
        btn_row.pack(fill="x", padx=40, pady=10)

        button_style = {
            "font": ("Segoe UI", 16, "bold"),
            "relief": "flat",
            "padx": 24,
            "pady": 12,
            "cursor": "hand2"
        }

        tk.Button(
            btn_row,
            text="⚡ Analyze",
            command=self.analyze,
            bg="#238636",
            fg="white",
            **button_style
        ).pack(side="left", padx=10)

        tk.Button(
            btn_row,
            text="🎲 Generate Password",
            command=self.generate_password,
            bg="#1f6feb",
            fg="white",
            **button_style
        ).pack(side="left", padx=10)

        tk.Button(
            btn_row,
            text="🗑 Clear",
            command=self.clear,
            bg="#30363d",
            fg="white",
            **button_style
        ).pack(side="left", padx=10)

        # NOTEBOOK
        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "TNotebook",
            background="#0d1117"
        )

        style.configure(
            "TNotebook.Tab",
            background="#21262d",
            foreground="#8b949e",
            font=("Segoe UI", 16, "bold"),
            padding=[24, 12]
        )

        self.nb = ttk.Notebook(self.root)

        self.nb.pack(fill="both", expand=True, padx=20, pady=10)

        self.tab_analysis = tk.Frame(self.nb, bg="#161b22")
        self.tab_hashes = tk.Frame(self.nb, bg="#161b22")

        self.nb.add(self.tab_analysis, text="📊 Analysis")
        self.nb.add(self.tab_hashes, text="🔑 Hashes")

        self.build_analysis_tab()
        self.build_hash_tab()

    # =========================
    # ANALYSIS TAB
    # =========================
    def build_analysis_tab(self):

        p = self.tab_analysis

        metrics = tk.Frame(p, bg="#161b22")
        metrics.pack(fill="x", padx=20, pady=20)

        self.score_card = self.metric_card(metrics, "Security Score", "—/7")
        self.entropy_card = self.metric_card(metrics, "Entropy", "—")
        self.crack_card = self.metric_card(metrics, "Crack Time", "—")
        self.length_card = self.metric_card(metrics, "Length", "—")

        # WARNINGS
        self.warn_label = tk.Label(
            p,
            text="No warnings",
            font=("Consolas", 15),
            bg="#161b22",
            fg="#f85149",
            justify="left"
        )

        self.warn_label.pack(anchor="w", padx=30, pady=20)

        # SUGGESTIONS
        self.sugg_label = tk.Label(
            p,
            text="Suggestions appear here",
            font=("Consolas", 15),
            bg="#161b22",
            fg="#ffa657",
            justify="left"
        )

        self.sugg_label.pack(anchor="w", padx=30)

    def metric_card(self, parent, title, value):

        card = tk.Frame(parent, bg="#21262d", padx=20, pady=20)

        card.pack(side="left", expand=True, fill="x", padx=10)

        tk.Label(
            card,
            text=title,
            font=("Consolas", 12),
            bg="#21262d",
            fg="#8b949e"
        ).pack()

        val = tk.Label(
            card,
            text=value,
            font=("Consolas", 24, "bold"),
            bg="#21262d",
            fg="#f0f6fc"
        )

        val.pack()

        return val

    # =========================
    # HASH TAB
    # =========================
    def build_hash_tab(self):

        p = self.tab_hashes

        self.hash_rows = {}

        for algo in ["MD5", "SHA-1", "SHA-256", "SHA-512", "BLAKE2b"]:

            row = tk.Frame(p, bg="#21262d", padx=15, pady=15)

            row.pack(fill="x", padx=20, pady=8)

            tk.Label(
                row,
                text=algo,
                font=("Consolas", 14, "bold"),
                bg="#21262d",
                fg="#58a6ff",
                width=10,
                anchor="w"
            ).pack(side="left")

            val = tk.Label(
                row,
                text="—",
                font=("Consolas", 12),
                bg="#21262d",
                fg="#c9d1d9",
                wraplength=800,
                justify="left"
            )

            val.pack(side="left", expand=True, fill="x")

            self.hash_rows[algo] = val

    # =========================
    # ACTIONS
    # =========================
    def live_update(self):

        pwd = self.entry.get()

        if not pwd:
            self.reset_bar()
            self.strength_label.config(text="—")
            return

        r = check_strength(pwd)

        self.update_bar(r["score"], r["color"])

        self.strength_label.config(
            text=r["strength"],
            fg=r["color"]
        )

    def analyze(self):

        pwd = self.entry.get()

        if not pwd:
            messagebox.showwarning("Empty", "Enter a password")
            return

        r = check_strength(pwd)

        hashes = generate_hashes(pwd)

        self.current_hashes = hashes

        self.score_card.config(text=f"{r['score']}/7")
        self.entropy_card.config(text=f"{r['entropy']} bits")
        self.crack_card.config(text=r["crack_time"])
        self.length_card.config(text=str(len(pwd)))

        if r["patterns"]:
            self.warn_label.config(
                text="\n".join(r["patterns"])
            )
        else:
            self.warn_label.config(
                text="✓ No risky patterns detected",
                fg="#3fb950"
            )

        if r["suggestions"]:
            self.sugg_label.config(
                text="\n".join(r["suggestions"])
            )
        else:
            self.sugg_label.config(
                text="✓ Excellent password",
                fg="#3fb950"
            )

        for algo, val in self.hash_rows.items():
            val.config(text=hashes.get(algo))

    def generate_password(self):

        pwd = generate_strong_password()

        self.entry.delete(0, tk.END)

        self.entry.insert(0, pwd)

        self.analyze()

        try:
            pyperclip.copy(pwd)
        except:
            pass

    def toggle_show(self):

        current = self.entry.cget("show")

        if current == "•":
            self.entry.config(show="")
            self.show_btn.config(text="🙈")
        else:
            self.entry.config(show="•")
            self.show_btn.config(text="👁")

    def clear(self):

        self.entry.delete(0, tk.END)

        self.strength_label.config(text="—")

        self.score_card.config(text="—/7")
        self.entropy_card.config(text="—")
        self.crack_card.config(text="—")
        self.length_card.config(text="—")

        self.warn_label.config(text="No warnings")
        self.sugg_label.config(text="Suggestions appear here")

        for algo, val in self.hash_rows.items():
            val.config(text="—")

        self.reset_bar()

    def update_bar(self, score, color):

        self.bar_canvas.update_idletasks()

        width = self.bar_canvas.winfo_width()

        fill = int((score / 7) * width)

        self.bar_canvas.delete("all")

        self.bar_canvas.create_rectangle(
            0,
            0,
            fill,
            16,
            fill=color,
            outline=""
        )

    def reset_bar(self):

        self.bar_canvas.delete("all")


# =========================
# RUN APP
# =========================
if __name__ == "__main__":

    root = tk.Tk()

    app = CipherGuardApp(root)

    root.mainloop()