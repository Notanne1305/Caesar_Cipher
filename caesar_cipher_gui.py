import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# ── Caesar Cipher Logic ────────────────────────────────────────────────────────

def caesar_cipher(text, shift, encrypt=True):
    direction = 1 if encrypt else -1
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - base + direction * (shift % 26)) % 26 + base)
        else:
            result += char
    return result

def caesar_encrypt(text, shift):
    return caesar_cipher(text, shift, encrypt=True)

def caesar_decrypt(text, shift):
    return caesar_cipher(text, shift, encrypt=False)

# ── Main App ───────────────────────────────────────────────────────────────────

class CaesarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Caesar Cipher")

        # ── Full screen setup ─────────────────────────────────────────────────
        self.state("zoomed")          # maximized on Windows
        self.update_idletasks()
        WIN_W = self.winfo_width()
        WIN_H = self.winfo_height()
        self.resizable(True, True)

        # ── Background image ──────────────────────────────────────────────────
        img_path = os.path.join(os.path.dirname(__file__), "Cesar_Montano.jpg")
        self._bg_label = tk.Label(self, bg="#1a1200")
        self._bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self._raw_img = None
        self._bg_photo = None
        try:
            self._raw_img = Image.open(img_path)
        except Exception as e:
            print(f"Warning: Could not load background image: {e}")
            self.configure(bg="#1a1200")

        # ── Dark overlay canvas ───────────────────────────────────────────────
        self._overlay = tk.Canvas(self, highlightthickness=0,
                                  bg="black")
        self._overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self._overlay.create_rectangle(0, 0, 9999, 9999,
                                       fill="#000000", stipple="gray25",
                                       tags="overlay_rect")

        # ── Central panel (uses place with rel coords so it stays centered) ───
        PANEL_W_REL = 0.55
        PANEL_H_REL = 0.82

        self._panel = tk.Frame(self, bg="#0d0b06",
                               highlightthickness=2,
                               highlightbackground="#8a6a1a")
        self._panel.place(relx=0.5, rely=0.5,
                          relwidth=PANEL_W_REL, relheight=PANEL_H_REL,
                          anchor="center")

        # Title
        tk.Label(self._panel, text="CAESAR CIPHER",
                 bg="#0d0b06", fg="#f5c842",
                 font=("Georgia", 26, "bold"),
                 pady=18).pack()

        tk.Frame(self._panel, bg="#8a6a1a", height=2).pack(fill="x", padx=30)

        # ── Notebook tabs ─────────────────────────────────────────────────────
        style = ttk.Style(self)
        style.theme_use("default")

        style.configure("Gold.TNotebook",
                        background="#0d0b06",
                        borderwidth=0)
        style.configure("Gold.TNotebook.Tab",
                        background="#1c1608",
                        foreground="#c8a03c",
                        font=("Georgia", 11, "bold"),
                        padding=[20, 8],
                        borderwidth=0)
        style.map("Gold.TNotebook.Tab",
                  background=[("selected", "#0d0b06")],
                  foreground=[("selected", "#f5c842")])

        nb = ttk.Notebook(self._panel, style="Gold.TNotebook")
        nb.pack(fill="both", expand=True, padx=24, pady=14)

        # ── Encrypt tab ───────────────────────────────────────────────────────
        enc_frame = tk.Frame(nb, bg="#0d0b06")
        nb.add(enc_frame, text="   Encrypt   ")
        self._build_cipher_tab(enc_frame, mode="encrypt")

        # ── Decrypt tab ───────────────────────────────────────────────────────
        dec_frame = tk.Frame(nb, bg="#0d0b06")
        nb.add(dec_frame, text="   Decrypt   ")
        self._build_cipher_tab(dec_frame, mode="decrypt")

        # ── Test Cases tab ────────────────────────────────────────────────────
        test_frame = tk.Frame(nb, bg="#0d0b06")
        nb.add(test_frame, text="   Test Cases   ")
        self._build_test_tab(test_frame)

        # ── Bind resize ───────────────────────────────────────────────────────
        self.bind("<Configure>", self._on_resize)
        self._update_bg()

    # ── Resize background image to fill window ────────────────────────────────
    def _update_bg(self):
        if self._raw_img is None:
            return
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 2 or h < 2:
            self.after(100, self._update_bg)  # Retry if window not ready
            return
        try:
            resized = self._raw_img.resize((w, h), Image.LANCZOS)
            self._bg_photo = ImageTk.PhotoImage(resized)
            self._bg_label.configure(image=self._bg_photo)
            self._bg_label.image = self._bg_photo  # Keep a reference
        except Exception as e:
            print(f"Error updating background: {e}")

    def _on_resize(self, event):
        if event.widget is self:
            self._update_bg()

    # ── Helper: label style ───────────────────────────────────────────────────
    def _lbl(self, parent, text, **kw):
        defaults = dict(bg="#0d0b06", fg="#c8a03c",
                        font=("Georgia", 11, "bold"),
                        anchor="w")
        defaults.update(kw)
        return tk.Label(parent, text=text, **defaults)

    # ── Build Encrypt / Decrypt tab ───────────────────────────────────────────
    def _build_cipher_tab(self, frame, mode):
        pad = dict(padx=28, pady=6)

        self._lbl(frame,
                  "Message to Encrypt:" if mode == "encrypt"
                  else "Ciphertext to Decrypt:").pack(fill="x", **pad)

        txt = tk.Text(frame, height=5, width=50,
                      bg="#1a1608", fg="#ffffff",
                      insertbackground="#f5c842",
                      relief="flat", highlightthickness=1,
                      highlightbackground="#5a4010",
                      font=("Consolas", 13),
                      wrap="word")
        txt.pack(fill="x", padx=28, pady=4)

        # Shift row
        shift_row = tk.Frame(frame, bg="#0d0b06")
        shift_row.pack(fill="x", **pad)

        self._lbl(shift_row, "Shift Key (0–25):").pack(side="left")

        shift_var = tk.IntVar(value=3)

        vcmd = (self.register(lambda v: v.isdigit() and 0 <= int(v) <= 25
                               if v else True), '%P')
        shift_entry = tk.Entry(shift_row, textvariable=shift_var,
                               width=4, bg="#1a1608", fg="#f5c842",
                               insertbackground="#f5c842",
                               relief="flat", highlightthickness=1,
                               highlightbackground="#5a4010",
                               font=("Consolas", 14),
                               justify="center",
                               validate="key", validatecommand=vcmd)
        shift_entry.pack(side="left", padx=(10, 16))

        slider = tk.Scale(shift_row, variable=shift_var,
                          from_=0, to=25, orient="horizontal",
                          length=260,
                          bg="#0d0b06", fg="#c8a03c",
                          troughcolor="#2a1e06",
                          highlightthickness=0,
                          showvalue=False,
                          sliderlength=18)
        slider.pack(side="left")

        # Result label
        self._lbl(frame, "Result:").pack(fill="x", padx=28, pady=(12, 2))

        result_var = tk.StringVar()
        result_entry = tk.Entry(frame, textvariable=result_var,
                                state="readonly",
                                bg="#0f0d04", fg="#f5c842",
                                readonlybackground="#0f0d04",
                                relief="flat", highlightthickness=1,
                                highlightbackground="#5a4010",
                                font=("Consolas", 13))
        result_entry.pack(fill="x", padx=28, pady=4)

        # Error label
        err_var = tk.StringVar()
        err_lbl = tk.Label(frame, textvariable=err_var,
                           bg="#0d0b06", fg="#f08080",
                           font=("Georgia", 10))
        err_lbl.pack(fill="x", padx=28)

        # Action button
        def run():
            msg = txt.get("1.0", "end-1c")
            if not msg.strip():
                err_var.set("Please enter a message.")
                result_var.set("")
                return
            try:
                shift = int(shift_var.get())
                if not (0 <= shift <= 25):
                    raise ValueError
            except (ValueError, tk.TclError):
                err_var.set("Shift key must be 0–25.")
                result_var.set("")
                return
            err_var.set("")
            fn = caesar_encrypt if mode == "encrypt" else caesar_decrypt
            result_var.set(fn(msg, shift))

        btn_text = "Encrypt  ▶" if mode == "encrypt" else "Decrypt  ▶"
        btn = tk.Button(frame, text=btn_text,
                        command=run,
                        bg="#b8892a", fg="#1a1200",
                        activebackground="#f5c842",
                        font=("Georgia", 13, "bold"),
                        relief="flat", padx=30, pady=10,
                        cursor="hand2")
        btn.pack(pady=(16, 6))

    # ── Build Test Cases tab ──────────────────────────────────────────────────
    def _build_test_tab(self, frame):
        canvas = tk.Canvas(frame, bg="#0d0b06", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical",
                                  command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg="#0d0b06")
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def on_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(win_id, width=canvas.winfo_width())

        inner.bind("<Configure>", on_configure)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))

        result_frame = tk.Frame(inner, bg="#0d0b06")
        result_frame.pack(fill="x", padx=16, pady=(14, 8))

        summary_var = tk.StringVar(value="Press 'Run Tests' to begin.")
        summary_lbl = tk.Label(result_frame, textvariable=summary_var,
                               bg="#0d0b06", fg="#c8a03c",
                               font=("Georgia", 10, "italic"))

        tests_container = tk.Frame(inner, bg="#0d0b06")
        tests_container.pack(fill="x", padx=16, pady=6)

        def run_tests():
            for w in tests_container.winfo_children():
                w.destroy()

            cases = [
                ("Test 1 — Basic Encryption (shift 3)",
                 "Hello, World!", 3, True, "Khoor, Zruog!", False),
                ("Test 2 — Basic Decryption (shift 3)",
                 "Khoor, Zruog!", 3, False, "Hello, World!", False),
                ("Test 3a — Large Shift (52 ≡ 0 mod 26)",
                 "ABC xyz", 52, True, "ABC xyz", False),
                ("Test 3b — Mixed Characters round-trip (shift 5)",
                 "Test123!@# With Numbers & Symbols", 5, True,
                 "Test123!@# With Numbers & Symbols", True),
                ("Test 3c — Wrap-around XYZ (shift 5)",
                 "XYZ", 5, True, "CDE", False),
                ("Test 3d — Full Round-trip (shift 13)",
                 "The Quick Brown Fox Jumps Over The Lazy Dog",
                 13, True,
                 "The Quick Brown Fox Jumps Over The Lazy Dog", True),
            ]

            passed = failed = 0

            for label, inp, shift, enc, expected, round_trip in cases:
                if round_trip:
                    encrypted = caesar_encrypt(inp, shift)
                    actual = caesar_decrypt(encrypted, shift)
                else:
                    actual = caesar_encrypt(inp, shift) if enc else caesar_decrypt(inp, shift)

                ok = actual == expected
                passed += ok
                failed += not ok

                row = tk.Frame(tests_container, bg="#141008",
                               highlightthickness=1,
                               highlightbackground="#3a2a08")
                row.pack(fill="x", pady=5)

                badge_color = "#4caf50" if ok else "#f44336"
                badge_text  = "PASS" if ok else "FAIL"

                header = tk.Frame(row, bg="#141008")
                header.pack(fill="x", padx=14, pady=(8, 3))

                tk.Label(header, text=label,
                         bg="#141008", fg="#c8a03c",
                         font=("Georgia", 10, "bold"),
                         anchor="w").pack(side="left")

                tk.Label(header, text=f" {badge_text} ",
                         bg=badge_color, fg="#fff",
                         font=("Consolas", 9, "bold")).pack(side="right")

                detail = tk.Frame(row, bg="#141008")
                detail.pack(fill="x", padx=14, pady=(0, 8))

                info = (f"Input: {inp[:40]}{'…' if len(inp)>40 else ''}   "
                        f"Shift: {shift}   "
                        f"Result: {actual[:40]}{'…' if len(actual)>40 else ''}")
                tk.Label(detail, text=info,
                         bg="#141008", fg="#ffffff" if ok else "#f08080",
                         font=("Consolas", 10),
                         anchor="w",
                         wraplength=600,
                         justify="left").pack(side="left")

            summary_var.set(f"Results: {passed} passed, {failed} failed.")
            summary_lbl.config(fg="#4caf50" if failed == 0 else "#f08080")

        run_btn = tk.Button(result_frame, text="▶  Run All Tests",
                            command=run_tests,
                            bg="#1c1608", fg="#c8a03c",
                            activebackground="#2e2010",
                            activeforeground="#f5c842",
                            font=("Georgia", 11, "bold"),
                            relief="flat", padx=18, pady=7,
                            cursor="hand2",
                            highlightthickness=1,
                            highlightbackground="#5a4010")
        run_btn.pack(side="left")
        summary_lbl.pack(side="left", padx=16)


if __name__ == "__main__":
    app = CaesarApp()
    app.mainloop()