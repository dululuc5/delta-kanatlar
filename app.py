from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
import io

app = Flask(__name__)

# Yönetici giriş bilgisi
KULLANICI = "admin"
SIFRE = "1234"

# Üyeler listesi
members = []

# Giriş sayfası
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == KULLANICI and password == SIFRE:
            return redirect("/panel")
        else:
            return render_template("login.html", error="Hatalı kullanıcı adı veya şifre")
    return render_template("login.html", error="")

# Panel sayfası
@app.route("/panel", methods=["GET", "POST"])
def panel():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        school_no = request.form.get("school_no")
        class_name = request.form.get("class")
        if name and phone and school_no and class_name:
            members.append({
                "name": name,
                "phone": phone,
                "school_no": school_no,
                "class": class_name
            })
    return render_template("panel.html", members=members)

# Excel olarak dışa aktar
@app.route("/export", methods=["POST"])
def export():
    df = pd.DataFrame(members)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Uyeler")
    output.seek(0)
    return send_file(output, download_name="uyeler.xlsx", as_attachment=True)

# GPT-2 simülasyonu: üyelerin isimlerini "GPT-2" etiketiyle tekrar gösterir
@app.route("/gpt2")
def gpt2_simulation():
    if not members:
        return "Henüz üye yok"
    repeated_names = [member['name'] + " GPT-2" for member in members]
    return "<br>".join(repeated_names)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
