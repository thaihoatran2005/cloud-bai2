import os
from functools import wraps
import pymysql
from dotenv import load_dotenv
from flask import Flask, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

def db():
    return pymysql.connect(
        host=os.environ["DB_HOST"], user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"], database=os.environ["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor, autocommit=True)

def need_login(f):
    @wraps(f)
    def w(*a, **k):
        if "uid" not in session:
            return jsonify(error="Chưa đăng nhập"), 401
        return f(*a, **k)
    return w

@app.post("/api/register")
def register():
    d = request.json
    try:
        with db() as c, c.cursor() as cur:
            cur.execute("INSERT INTO users(username,password_hash) VALUES(%s,%s)",
                        (d["username"], generate_password_hash(d["password"])))
    except pymysql.err.IntegrityError:
        return jsonify(error="Tên đã tồn tại"), 400
    return jsonify(ok=True)

@app.post("/api/login")
def login():
    d = request.json
    with db() as c, c.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE username=%s", (d["username"],))
        u = cur.fetchone()
    if not u or not check_password_hash(u["password_hash"], d["password"]):
        return jsonify(error="Sai tài khoản hoặc mật khẩu"), 401
    session["uid"] = u["id"]
    return jsonify(ok=True)

@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify(ok=True)

@app.get("/api/notes")
@need_login
def list_notes():
    with db() as c, c.cursor() as cur:
        cur.execute("SELECT id,title,content FROM notes WHERE user_id=%s ORDER BY id DESC",
                    (session["uid"],))
        return jsonify(cur.fetchall())

@app.post("/api/notes")
@need_login
def add_note():
    d = request.json
    with db() as c, c.cursor() as cur:
        cur.execute("INSERT INTO notes(user_id,title,content) VALUES(%s,%s,%s)",
                    (session["uid"], d["title"], d.get("content", "")))
    return jsonify(ok=True)

@app.put("/api/notes/<int:nid>")
@need_login
def edit_note(nid):
    d = request.json
    with db() as c, c.cursor() as cur:
        cur.execute("UPDATE notes SET title=%s,content=%s WHERE id=%s AND user_id=%s",
                    (d["title"], d.get("content", ""), nid, session["uid"]))
    return jsonify(ok=True)

@app.delete("/api/notes/<int:nid>")
@need_login
def del_note(nid):
    with db() as c, c.cursor() as cur:
        cur.execute("DELETE FROM notes WHERE id=%s AND user_id=%s", (nid, session["uid"]))
    return jsonify(ok=True)
