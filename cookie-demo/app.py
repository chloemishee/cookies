from uuid import uuid4

from flask import Flask, make_response, redirect, render_template, request, url_for

app = Flask(__name__)


active_sessions = {}

stolen_cookies = []


def create_session(username, mode):
    """Makes a fake session id and saves the user info."""
    session_id = str(uuid4())
    active_sessions[session_id] = {
        "username": username,
        "mode": mode,
    }
    return session_id


def get_current_session():
    """Gets the cookie from the browser and matches it to the session dict."""
    session_id = request.cookies.get("session_id")
    if not session_id:
        return None, None

    session_data = active_sessions.get(session_id)
    return session_id, session_data


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    mode = request.form.get("mode", "vulnerable")

    if not username:
        return render_template(
            "login.html",
            error="Please enter a username.",
        )

    session_id = create_session(username, mode)
    response = make_response(redirect(url_for("dashboard")))

    if mode == "secure":
        # more secure version
        # HttpOnly matters here because JS should not be able to read the session cookie
        response.set_cookie(
            "session_id",
            session_id,
            httponly=True,
            secure=False,
            samesite="Strict",
        )
    else:
        # vulnerable version
        # no HttpOnly means document.cookie can see the session_id
        response.set_cookie("session_id", session_id)

    return response


@app.route("/dashboard")
def dashboard():
    session_id, session_data = get_current_session()
    if not session_data:
        return redirect(url_for("index"))

    is_secure_mode = session_data["mode"] == "secure"
    return render_template(
        "dashboard.html",
        username=session_data["username"],
        mode=session_data["mode"],
        is_secure_mode=is_secure_mode,
        session_id=session_id,
    )
# we can use editthiscookie extension to simulate a hijacking


@app.route("/steal", methods=["POST"])
def steal():
    # this is acting like the attacker side
    # in the weak version the page JS can send document.cookie here
    stolen_value = request.form.get("stolen_cookie", "").strip()
    mode = request.form.get("mode", "unknown")
    source_user = request.form.get("username", "unknown")

    if stolen_value:
        stolen_cookies.append(
            {
                "cookie": stolen_value,
                "mode": mode,
                "username": source_user,
            }
        )

    return {"status": "received", "stolen_cookie": stolen_value}


@app.route("/attacker")
def attacker():
    return render_template("attacker.html", stolen_cookies=stolen_cookies)


@app.route("/logout")
def logout():
    session_id, session_data = get_current_session()
    if session_id and session_data:
        active_sessions.pop(session_id, None)

    response = make_response(redirect(url_for("index")))
    response.delete_cookie("session_id")
    return response


if __name__ == "__main__":
    print("Starting demo")
    print("Use vulnerable mode to show cookie theft.")
    print("Use secure mode to show how HttpOnly blocks JavaScript access.")
    app.run(debug=True)


