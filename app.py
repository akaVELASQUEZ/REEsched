import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///schedule.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """User Registration"""

    # Get inputs from user
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        confirmUser = db.execute("SELECT username FROM users")

        #Validates the inputs
        if not username:
            return apology("must provide username", 400)

        if not password:
            return apology("must provide password", 400)

        for i in range(len(confirmUser)):
            if username == confirmUser[i]['username']:
                return apology("username already exist", 400)

        if password != confirmation:
            return apology("passwords does not match", 400)

        # Generate a hash for the password
        hash = generate_password_hash(password)

        # Inserts the user details to the database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
        id = db.execute("SELECT id FROM users WHERE username = ?" , username)

        # Logs the user to a session
        session["user_id"] = id[0]["id"]
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create a panel based on user's inputs"""

    # Get's data of the circuits from the user
    if request.method == "POST":

        # Save's the input from user to a variable
        panelName = request.form.get("panelName")
        voltage = request.form.get("voltage")
        lighting = request.form.getlist("lighting")
        outlet = request.form.getlist("outlet")
        appliance = request.form.getlist("appliance")
        rating = request.form.getlist("rating")

        # Insert's the data to panels table on the database
        panels = db.execute("SELECT panel FROM panels WHERE user_id = ?", session["user_id"])

        # Validates the input if there's no duplicates
        for i in range(len(panels)):
            if panelName == panels[i]['panel']:
                return apology("panel name already exist", 400)
        a = len(lighting)
        acu = ['acu', 'aircon', 'air conditioning unit', 'accu']
        totalCurrent = 0
        highest = 0

        # Get's the panel ID from the panels table
        db.execute("INSERT INTO panels (user_id, panel) VALUES(?, ?)", session["user_id"], panelName)
        ID = db.execute("SELECT id FROM panels WHERE panel = ? and user_id = ?", panelName, session["user_id"])
        panelID =ID[0]["id"]

        # Since more or less the input we'll get is a list, for loop would be used to check all inputs.
        for i in range(a):

            # Declaration of variables
            power = 0
            current = 0
            description = ""
            conductor = ""
            AT = 0
            AF = 0
            poles = 1
            Mconductor = ""
            ATm = 0
            AFm = 0

            # Check's if there's a lighting load input on a circuit
            if lighting[i] != '':
                lighting[i] = int(lighting[i])
                power = lighting[i] * 100
                if outlet[i] == '' and appliance[i] == '' :
                    description = 'Lighting Outlet '
                else:
                    description = 'Lighting Outlet & '

            # Check's if there's a CO load input on a circuit
            if outlet[i] != '':
                outlet[i] = int(outlet[i])
                power = power + (outlet[i] * 180)
                if appliance[i] == '' :
                    description = description + 'Convenience Outlet'
                else:
                    description = description + 'Convenience Outlet & '

            # Check's if there's a appliance load input on a circuit
            if appliance[i] != '':
                rating[i] = float(rating[i])

                # The code uses different rating for ACU which is a continuous motor load. This is to check the type
                # of appliance load the user input
                if appliance[i].lower() in acu:
                    hp = rating[i]
                    rating[i] = float((rating[i])/746)
                    rating[i] = round(rating[i], 2)

                    # Check's the rating and load of the ACU
                    if rating[i] == 0.17:
                        rating[i] = int(voltage) * 2.2
                    elif rating[i] == 0.25:
                        rating[i] = int(voltage) * 2.9
                    elif rating[i] == 0.33:
                        rating[i] = int(voltage) * 3.6
                    elif rating[i] == 0.5:
                        rating[i] = int(voltage) * 4.9
                    elif rating[i] == 0.75:
                        rating[i] = int(voltage) * 6.9
                    elif rating[i] == 1:
                        rating[i] = int(voltage) * 8
                    elif rating[i] == 1.5:
                        rating[i] = int(voltage) * 10
                    elif rating[i] == 2:
                        rating[i] = int(voltage) * 12
                    elif rating[i] == 3:
                        rating[i] = int(voltage) * 17
                    elif rating[i] == 5:
                        rating[i] = int(voltage) * 28
                    elif rating[i] == 7.5:
                        rating[i] = int(voltage) * 40
                    elif rating[i] == 10:
                        rating[i] = int(voltage) * 50
                    else:
                        rating[i] = ((4.88821 * rating[i]) + 2.4311) * int(voltage)
                    rate = rating[i]
                    power = power + (rating[i])
                    description = description + 'ACU ' + str(round(hp/746, 2)) + 'HP'

                # If the input is not ACU, the computation for normal appliance would apply
                else:
                    rate = rating[i]
                    power = power + rating[i]
                    description = description + str(appliance[i]) + " " + str(round(rating[i]/1000, 2)) + 'KW'

                # Check's the highest rated appliance. Would be used in the later computation
                if rate > highest:
                    highest = rate

            # Selects the appropriate circuit protection of the circuit.
            current = power/int(voltage)
            current = round(current, 2)
            totalCurrent = totalCurrent + current

            # The circuit breaker for ACU uses a table for computing the load. This is to check if the load is ACU
            if appliance[i].lower() in acu:
                if current < 12 :
                    AT = 20
                    AF = 63
                    conductor = "3-3.5mm² Cu-THHN"
                elif current < 24 and current >= 12:
                    AT = 30
                    AF = 63
                    conductor = "2-5.5mm² & 1-3.5mm² Cu-THHN"
                elif current < 32 and current >= 24:
                    AT = 40
                    AF = 63
                    conductor = "2-5.5mm² & 1-3.5mm² Cu-THHN"
                elif current < 40 and current >= 32:
                    AT = 50
                    AF = 63
                    conductor = "2-8.0mm² & 1-5.5mm² Cu-THHN"
                elif current < 50.1 and current >= 40:
                    AT = 63
                    AF = 63
                    conductor = "2-8.0mm² & 1-5.5mm² Cu-THHN"

            # If the load is not ACU, proceed to the table for normal loads
            else:
                if current < 12:
                    AT = 15
                    AF = 63
                    conductor = "3-3.5mm² Cu-THHN"
                elif current < 16 and current >= 12:
                    AT = 20
                    AF = 63
                    conductor = "3-3.5mm² Cu-THHN"
                elif current < 24 and current >= 16:
                    AT = 30
                    AF = 63
                    conductor = "2-5.5mm² & 1-3.5mm² Cu-THHN"
                elif current < 32 and current >= 24:
                    AT = 40
                    AF = 63
                    conductor = "2-5.5mm² & 1-3.5mm² Cu-THHN"
                elif current < 40 and current >= 32:
                    AT = 50
                    AF = 63
                    conductor = "2-8.0mm² & 1-5.5mm² Cu-THHN"
                elif current < 50.1 and current >= 40:
                    AT = 63
                    AF = 63
                    conductor = "2-14.0mm² & 1-8.0mm² Cu-THHN"

            # Insert the data to the circuits table of the database
            db.execute("INSERT INTO circuits VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        session["user_id"], panelID, i + 1, description, voltage, poles, AT, AF, current,
                        '','' ,'' , conductor)

        # After checking each circuits, the computation for main breaker would be done
        FLC = round((totalCurrent * 0.8) + ((highest/int(voltage)) * 0.25), 2)
        totalCurrent = round(totalCurrent, 2)
        if FLC < 12:
            ATm = 15
            AFm = 63
            Mconductor = "3-3.5mm² Cu-THHN"
        elif FLC < 16 and FLC >= 12:
            ATm = 20
            AFm = 63
            Mconductor = "3-3.5mm² Cu-THHN"
        elif FLC < 24 and FLC >= 16:
            ATm = 30
            AFm = 63
            Mconductor = "2-5.5mm² & 1-3.5mm² Cu-THHN"
        elif FLC < 32 and FLC >= 24:
            ATm = 40
            AFm = 63
            Mconductor = "2-5.5mm² & 1-3.5mm² Cu-THHN"
        elif FLC < 40 and FLC >= 32:
            ATm = 50
            AFm = 63
            Mconductor = "2-8.0mm² & 1-5.5mm² Cu-THHN"
        elif FLC < 50.1 and FLC >= 40:
            ATm = 63
            AFm = 63
            Mconductor = "2-14.0mm² & 1-8.0mm² Cu-THHN"
        elif FLC < 64 and FLC >= 50.1:
            ATm = 80
            AFm = 125
            Mconductor = "2-22.0mm² & 1-8.0mm² Cu-THHN"

        # Insert the main breaker data to the database
        db.execute("INSERT INTO mains VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        session["user_id"], panelID, panelName, panelName, voltage, poles, ATm, AFm, totalCurrent,
                        '', '' ,'' ,FLC, Mconductor)
        return redirect("/")
    else:
        return render_template("create.html")


@app.route("/")
@login_required
def index():
    """Show's all the main circuit of the panel's you've created"""

    # Go to the mains table and get each main breaker panel's the user created
    mains = db.execute("SELECT panel_id, panel_name, voltage, poles, trip, frame, aphase, bphase, cphase, threephase, totalcurrent, conductor FROM mains WHERE user_id = ?", session["user_id"])
    return render_template("index.html", mains=mains)


@app.route("/panels", methods=["GET", "POST"])
@login_required
def panels():
    """Used for viewing the circuit details or deleting a panel"""

    # Show's a selection of the panel's the user created and button's for deleting or viewing its contents.
    if request.method == "POST":

        # If the button pressed is view, shows the details of selected panel
        if request.form.get("button") == "VIEW":
            name = request.form.get("panel")
            panel_id = db.execute("SELECT id FROM panels WHERE panel = ? AND user_id = ?", name, session["user_id"])
            panel_id = panel_id[0]['id']
            circuits = db.execute("SELECT panel_id, circuit, description, voltage, poles, trip, frame, aphase, bphase, cphase, threephase, pconductor FROM circuits WHERE panel_id = ?", panel_id)
            return render_template("circuits.html", circuits=circuits)

        # If the button pressed is delete, delete the panel details on all the table of the database
        elif request.form.get("button") == "DELETE":
            name = request.form.get("panel")
            panel_id = db.execute("SELECT id FROM panels WHERE panel = ? AND user_id = ?", name, session["user_id"])
            panel_id = panel_id[0]['id']
            db.execute("DELETE FROM mains WHERE panel_id = ?", panel_id)
            db.execute("DELETE FROM circuits WHERE panel_id = ?", panel_id)
            db.execute("DELETE FROM panels WHERE id = ?", panel_id)
            return redirect("/")
    else:
        panels = db.execute("SELECT panel_name FROM mains WHERE user_id = ?", session["user_id"])
        return render_template("view.html", panels=panels)


@app.route("/help")
@login_required
def help():
    """Tutorial page"""
    return render_template("help.html")