from flask import Flask, redirect, render_template, request, session, url_for, flash
from flask_session import Session
from datetime import timedelta, datetime
import mysql.connector
from contextlib import contextmanager
from functools import wraps
from flask import abort
import os


app = Flask(__name__)


app.secret_key = "CHANGE_ME_TO_A_RANDOM_SECRET"

session_dir = os.path.join(app.root_path, "flask_session_data")
os.makedirs(session_dir, exist_ok=True)

app.config.update(
    SESSION_TYPE="filesystem",
    SESSION_FILE_DIR="/flask_session_data",
    SESSION_PERMANENT=True,
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=10),
    SESSION_REFRESH_EACH_REQUEST=True,
    SESSION_COOKIE_SECURE=False
)

Session(app)

@contextmanager
def db_curr():
    mydb=None
    cursor= None
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootroot",
            database="flytau_db",
            autocommit=True
        )
        cursor=mydb.cursor()
        yield cursor
    except mysql.connector.Error as err:
        raise err
    finally:
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()


def next_id(cursor, table, col):
    cursor.execute(f"SELECT COALESCE(MAX({col}), 0) + 1 FROM {table}")
    return cursor.fetchone()[0]


def _mysql_time_to_timeobj(t):
    # mysql TIME sometimes comes as timedelta in your project
    if isinstance(t, timedelta):
        total_seconds = int(t.total_seconds())
        hours = (total_seconds // 3600) % 24
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return datetime.strptime(f"{hours:02d}:{minutes:02d}:{seconds:02d}", "%H:%M:%S").time()
    return t

@app.route('/', methods = ['POST','GET'])
def home_page():
    if request.method == 'POST':
        first_name=request.form.get("first_name")
        last_name = request.form.get("last_name")
        password = request.form.get("pass")
        return render_template('home_page.html', first_name=first_name, last_name=last_name,password=password)
    else:
        return render_template('home_page.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('sign_up_form.html')

    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    phone = request.form.get("phone", "").strip()
    passport = request.form.get("passport", "").strip()
    date_of_birth = request.form.get("date_of_birth", "").strip()

    if not all([first_name, last_name, email, password, phone, passport, date_of_birth]):
        return render_template('sign_up_form.html', error="Please fill all fields.")

    try:
        with db_curr() as cursor:
            cursor.execute("SELECT 1 FROM Client WHERE Email_ID = %s LIMIT 1", (email,))
            exists_in_client = cursor.fetchone() is not None

            cursor.execute("SELECT 1 FROM Registered WHERE Email_R_ID = %s LIMIT 1", (email,))
            exists_in_registered = cursor.fetchone() is not None

            if exists_in_registered:
                return render_template('sign_up_form.html', error="This email is already registered. Please login.")

            if not exists_in_client:
                cursor.execute("INSERT INTO Client (Email_ID) VALUES (%s)", (email,))

            cursor.execute("""
                INSERT INTO Registered
                (Email_R_ID, Registration_date, Date_of_birth, Passport_number,
                 Phone_number, First_Name, Last_Name, Password)
                VALUES (%s, CURDATE(), %s, %s, %s, %s, %s, %s)
            """, (email, date_of_birth, passport, phone, first_name, last_name, password))

    except mysql.connector.Error as err:
        return render_template('sign_up_form.html', error=f"Database error: {err}")

    session.clear()
    session["role"] = "customer"
    session["email"] = email
    session["first_name"] = first_name
    session["last_name"] = last_name

    return redirect(url_for("home_page"))



@app.route('/login/customer', methods=['GET', 'POST'])
def login_customer():
    if request.method == 'GET':
        return render_template('login_customer.html')

    customer_email = request.form.get("customer_email")
    customer_password = request.form.get("customer_password")

    if customer_email and customer_password:
        with db_curr() as cursor:
            cursor.execute("""
                SELECT Email_R_ID, First_Name, Last_Name
                FROM Registered
                WHERE Email_R_ID = %s AND Password = %s
                LIMIT 1
            """, (customer_email, customer_password))
            row = cursor.fetchone()

        if not row:
            return render_template('login_customer.html', error="Invalid customer email/password")

        session.clear()
        session["role"] = "customer"
        session["email"] = row[0]
        session["first_name"] = row[1]
        session["last_name"] = row[2]
        return redirect(url_for("home_page"))

    return render_template('login_customer.html', error="Please fill all fields.")

@app.route('/login/manager', methods=['GET', 'POST'])
def login_manager():
    if request.method == 'GET':
        return render_template('login_manager.html')

    manager_id = request.form.get("manager_id")
    manager_password = request.form.get("manager_password")

    if manager_id and manager_password:
        with db_curr() as cursor:
            cursor.execute("""
                SELECT e.E_ID, e.FirstName, e.LastName
                FROM Manger m
                JOIN Employee e ON e.E_ID = m.E_ID
                WHERE m.E_ID = %s AND m.Password = %s
                LIMIT 1
            """, (manager_id, manager_password))
            row = cursor.fetchone()

        if not row:
            return render_template('login_manager.html', error="Invalid manager ID/password")

        session.clear()
        session["role"] = "manager"
        session["manager_e_id"] = row[0]
        session["first_name"] = row[1]
        session["last_name"] = row[2]
        return redirect(url_for("manager"))

    return render_template('login_manager.html', error="Please fill all fields.")


def login_required(role=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if "role" not in session:
                return redirect(url_for("login_customer"))
            if role and session.get("role") != role:
                return abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home_page"))

@app.route('/manager')
@login_required(role="manager")
def manager():
    return render_template('managers.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    with db_curr() as cursor:
        cursor.execute("SELECT Airport_Name FROM Airport ORDER BY Airport_Name")
        airports = [row[0] for row in cursor.fetchall()]

    if request.method == 'GET':
        return render_template('search_flights.html', airports=airports, num_tickets=1)

    source = request.form.get('source')
    dest = request.form.get('dest')
    date = request.form.get('date')
    num_tickets = request.form.get('num_tickets', type=int)

    if not source or not dest:
        return render_template('search_flights.html', airports=airports, num_tickets=num_tickets or 1,
                               error="Please select both source and destination.")

    if not num_tickets or num_tickets < 1:
        return render_template('search_flights.html', airports=airports, num_tickets=1,
                               error="Please choose a valid number of tickets.")

    base_query = """
        SELECT f.F_ID, f.Status, f.Type,
               f.Date_of_flight, f.Time_of_flight,
               f.Date_of_Arrival, f.Time_of_Arrival
        FROM Flight f
        JOIN Route r ON f.R_ID = r.R_ID
        WHERE r.Airport_Name_Source = %s
          AND r.Airport_Name_Dest = %s
          AND f.Status IN ('Active', 'Scheduled')
          AND TIMESTAMP(f.Date_of_flight, f.Time_of_flight) >= NOW()
          AND (
                SELECT COUNT(*)
                FROM Seat s
                WHERE s.A_ID = f.A_ID
                  AND NOT EXISTS (
                    SELECT 1
                    FROM Flight_Ticket t
                    WHERE t.F_ID = f.F_ID
                      AND t.Seat_A_ID = s.A_ID
                      AND t.Seat_Column = s.Column_Num
                      AND t.Seat_Row = s.Row_Num
                      AND t.Seat_Class_Type = s.Class_Type
                  )
              ) >= %s
    """

    params = [source, dest, num_tickets]

    if date:
        base_query += " AND f.Date_of_flight = %s"
        params.append(date)

    base_query += " ORDER BY f.Date_of_flight, f.Time_of_flight"

    with db_curr() as cursor:
        cursor.execute(base_query, tuple(params))
        rows = cursor.fetchall()

    flights = [
        {
            "F_ID": r[0],
            "Status": r[1],
            "Type": r[2],
            "Date_of_flight": r[3],
            "Time_of_flight": r[4],
            "Date_of_Arrival": r[5],
            "Time_of_Arrival": r[6],
        }
        for r in rows
    ]

    return render_template(
        'search_results.html',
        flights=flights,
        source=source,
        dest=dest,
        date=date if date else "Any date",
        num_tickets=num_tickets
    )


@app.route('/select-flight', methods=['POST'])
def select_flight():
    if session.get("role") == "manager":
        return redirect(url_for("search"))

    flight_id = request.form.get("flight_id")
    num_tickets = request.form.get("num_tickets", type=int)

    if not flight_id or not num_tickets or num_tickets < 1:
        return redirect(url_for("search"))

    return redirect(url_for("choose_seats", flight_id=flight_id, num_tickets=num_tickets))


@app.route('/choose-seats', methods=['GET', 'POST'])
def choose_seats():
    if session.get("role") == "manager":
        return redirect(url_for("search"))

    if request.method == 'POST':
        flight_id = request.form.get("flight_id")
        num_tickets = request.form.get("num_tickets", type=int)
    else:
        flight_id = request.args.get("flight_id")
        num_tickets = request.args.get("num_tickets", type=int)

    if not flight_id or not num_tickets or num_tickets < 1:
        return redirect(url_for("search"))

    # ✅ Bring also ticket prices
    query_flight = """
        SELECT A_ID, regular_ticket_price, business_ticket_price
        FROM Flight
        WHERE F_ID=%s
        LIMIT 1
    """

    query_seats = """
        SELECT s.Column_Num, s.Row_Num, s.Class_Type
        FROM Seat s
        WHERE s.A_ID = %s
          AND NOT EXISTS (
            SELECT 1
            FROM Flight_Ticket t
            WHERE t.F_ID = %s
              AND t.Seat_A_ID = s.A_ID
              AND t.Seat_Column = s.Column_Num
              AND t.Seat_Row = s.Row_Num
              AND t.Seat_Class_Type = s.Class_Type
          )
        ORDER BY s.Class_Type, s.Row_Num, s.Column_Num
    """

    with db_curr() as cursor:
        cursor.execute(query_flight, (flight_id,))
        row = cursor.fetchone()
        if not row:
            return redirect(url_for("search"))

        airplane_id = row[0]
        regular_price = float(row[1] or 0)
        business_price = float(row[2] or 0)

        cursor.execute(query_seats, (airplane_id, flight_id))
        seats = cursor.fetchall()

    seat_items = []
    for col, row_num, class_type in seats:
        cls = (class_type or "").lower()
        price = business_price if cls == "business" else regular_price

        seat_items.append({
            "col": col,
            "row": row_num,
            "class": class_type,
            "price": float(price),
            "value": f"{col}|{row_num}|{class_type}"
        })

    session["last_seats"] = seat_items

    if num_tickets > len(seat_items):
        return render_template(
            "choose_seats.html",
            seats=seat_items,
            flight_id=flight_id,
            num_tickets=num_tickets,
            regular_price=regular_price,
            business_price=business_price,
            error=f"Only {len(seat_items)} seats are available."
        )

    return render_template(
        "choose_seats.html",
        seats=seat_items,
        flight_id=flight_id,
        num_tickets=num_tickets,
        regular_price=regular_price,
        business_price=business_price
    )


@app.route('/book-selected-seats', methods=['POST'])
def book_selected_seats():
    flight_id = request.form.get("flight_id")
    num_tickets = request.form.get("num_tickets", type=int)
    selected = request.form.getlist("seats")

    # Basic validation before saving to session or proceeding
    if not flight_id or not num_tickets or num_tickets < 1:
        return redirect(url_for("search"))
    if len(selected) != num_tickets:
        seat_items = session.get("last_seats", [])
        return render_template(
            "choose_seats.html",
            seats=seat_items,
            flight_id=flight_id,
            num_tickets=num_tickets,
            error=f"Please select exactly {num_tickets} seat(s)."
        )

    # Block managers explicitly
    if session.get("role") == "manager":
         flash("Administrators cannot make reservations.", "error")
         return redirect(url_for("manager"))

    # Guest Handling: If not logged in, save intent and redirect to guest login
    if not session.get("role"):
        session["pending_booking"] = {
            "flight_id": flight_id,
            "num_tickets": num_tickets,
            "seats": selected
        }
        return redirect(url_for("guest_login"))

    customer_email = session.get("email") or session.get("customer_email")
    if not customer_email: # Should not happen if role is set, but as a fallback
        return redirect(url_for("login_customer"))
    return _perform_booking(customer_email, flight_id, num_tickets, selected)

@app.route('/guest-login', methods=['GET'])
def guest_login():
    return render_template('guest_login.html')

@app.route('/guest-login', methods=['POST'])
def guest_login_post():
    email = request.form.get("guest_email")
    if not email:
        return render_template('guest_login.html', error="Email is required")

    # DB: Ensure Client + Guest exist
    with db_curr() as cursor:
        # Insert into Client if not exists (assuming structure ok, minimal fields)
        # We only have email. We might need other fields if Client requires them. 
        # Checking schema: Client constraints? Assuming minimal insert works or we dummy fill.
        # But wait, Registered extends Client. Guest extends Client.
        # If Client requires First/Last name, we might fail.
        # Let's hope Client just needs Email_ID. 
        # If not, we might need a fuller form.
        # SQL Dump showed Registered has First/Last. Client schema is unknown but usually parent has shared fields.
        # If Client has First/Last, we need to ask for them.
        # I'll try simple insert first.
        try:
            cursor.execute("INSERT IGNORE INTO Client (Email_ID) VALUES (%s)", (email,))
            cursor.execute("INSERT IGNORE INTO Guest (Email_G_ID) VALUES (%s)", (email,))
        except mysql.connector.Error as err:
             return render_template('guest_login.html', error=f"Database error: {err}")

    session["role"] = "guest"
    session["email"] = email
    session["first_name"] = "Guest" # Placeholder
    session["last_name"] = "" 

    # Resume booking if pending
    pending = session.get("pending_booking")
    if pending:
        # Clear pending after retrieving
        flight_id = pending["flight_id"]
        num_tickets = pending["num_tickets"]
        seats = pending["seats"]
        session.pop("pending_booking", None)
        return _perform_booking(email, flight_id, num_tickets, seats)
    
    return redirect(url_for("home_page"))

def _perform_booking(customer_email, flight_id, num_tickets, selected):
    # Re-verify counts
    if len(selected) != num_tickets:
         return redirect(url_for("search")) # Or better error handling

    parsed = []
    for v in selected:
        col, row_str, class_type = v.split("|")
        parsed.append((col, int(row_str), class_type))

    with db_curr() as cursor:
        cursor.execute("SELECT A_ID, regular_ticket_price, business_ticket_price FROM Flight WHERE F_ID=%s LIMIT 1", (flight_id,))
        fr = cursor.fetchone()
        if not fr:
            return redirect(url_for("search"))
        airplane_id = fr[0]
        regular_price_val = float(fr[1] or 0)
        business_price_val = float(fr[2] or 0)

        check_seat_available = """
            SELECT 1
            FROM Seat s
            WHERE s.A_ID=%s AND s.Column_Num=%s AND s.Row_Num=%s AND s.Class_Type=%s
              AND NOT EXISTS (
                SELECT 1 FROM Flight_Ticket t
                WHERE t.F_ID=%s
                  AND t.Seat_A_ID=s.A_ID
                  AND t.Seat_Column=s.Column_Num
                  AND t.Seat_Row=s.Row_Num
                  AND t.Seat_Class_Type=s.Class_Type
              )
            LIMIT 1
        """

        calc_total_price = 0.0
        for col, row_num, class_type in parsed:
            cursor.execute(check_seat_available, (airplane_id, col, row_num, class_type, flight_id))
            if not cursor.fetchone():
                return render_template("booking_success.html", error="One or more selected seats are no longer available.")
            
            if class_type.lower() == 'business':
                calc_total_price += business_price_val
            else:
                calc_total_price += regular_price_val

        calc_cancellation_fee = calc_total_price * 0.05

        cursor.execute("SELECT COALESCE(MAX(B_ID), 0) + 1 FROM Booking")
        booking_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO Booking (B_ID, Status, Price, Cancellation_Fee, booking_date, booking_time, Client_Email)
            VALUES (%s, %s, %s, %s, CURDATE(), CURTIME(), %s)
            """,
            (booking_id, "Confirmed", calc_total_price, calc_cancellation_fee, customer_email)
        )

        cursor.execute("SELECT COALESCE(MAX(Ticket_ID), 0) + 1 FROM Flight_Ticket")
        next_ticket_id = cursor.fetchone()[0]

        tickets_created = []
        for col, row_num, class_type in parsed:
            cursor.execute(
                """
                INSERT INTO Flight_Ticket
                (Ticket_ID, Status, Seat_Column, Seat_Row, Seat_A_ID, Seat_Class_Type, F_ID, B_ID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (next_ticket_id, "Confirmed", col, row_num, airplane_id, class_type, flight_id, booking_id)
            )
            tickets_created.append({"ticket_id": next_ticket_id, "col": col, "row": row_num, "class": class_type})
            next_ticket_id += 1

    return render_template(
        "booking_success.html",
        booking_id=booking_id,
        flight_id=flight_id,
        tickets=tickets_created,
        mode="selected"
    )

@app.route('/my-bookings')
def my_bookings():
    if session.get("role") != "customer":
        return redirect(url_for("login_customer"))

    email = session.get("email")
    if not email:
        return redirect(url_for("login_customer"))

    query = """
        SELECT
            b.B_ID,
            b.Status,
            b.booking_date,
            b.booking_time,
            COUNT(t.Ticket_ID) AS tickets_count,
            MIN(t.F_ID) AS any_flight_id,
            MIN(f.Date_of_flight) AS flight_date,
            MIN(f.Time_of_flight) AS flight_time
        FROM Booking b
        JOIN Flight_Ticket t ON t.B_ID = b.B_ID
        JOIN Flight f ON f.F_ID = t.F_ID
        WHERE b.Client_Email = %s
          AND b.Status != 'Cancelled'
        GROUP BY b.B_ID, b.Status, b.booking_date, b.booking_time
        ORDER BY flight_date DESC, flight_time DESC
    """

    with db_curr() as cursor:
        cursor.execute(query, (email,))
        rows = cursor.fetchall()

    bookings = []
    for r in rows:
        bookings.append({
            "B_ID": r[0],
            "Status": r[1],
            "booking_date": r[2],
            "booking_time": r[3],
            "tickets_count": r[4],
            "F_ID": r[5],
            "Date_of_flight": r[6],
            "Time_of_flight": r[7],
        })

    # Split to upcoming/past based on current date+time
    now = datetime.now()
    upcoming = []
    past = []

    for b in bookings:
        t = b["Time_of_flight"]

        # mysql TIME sometimes comes as timedelta
        if isinstance(t, timedelta):
            total_seconds = int(t.total_seconds())
            hours = (total_seconds // 3600) % 24
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            t = datetime.strptime(f"{hours:02d}:{minutes:02d}:{seconds:02d}", "%H:%M:%S").time()

        flight_dt = datetime.combine(b["Date_of_flight"], t)

        if flight_dt >= now:
            upcoming.append(b)
        else:
            past.append(b)

    # Sort nicer:
    upcoming.sort(key=lambda x: (x["Date_of_flight"], x["Time_of_flight"]))        # nearest first
    past.sort(key=lambda x: (x["Date_of_flight"], x["Time_of_flight"]), reverse=True)  # newest past first

    return render_template("my_booking.html", upcoming=upcoming, past=past)


@app.route("/cancel-booking/<int:booking_id>", methods=["POST"])
def cancel_booking(booking_id):
    if session.get("role") != "customer":
        return redirect(url_for("login_customer"))

    email = session.get("email")
    if not email:
        return redirect(url_for("login_customer"))

    # Transaction: delete tickets first, then booking
    mydb = None
    cursor = None

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootroot",
            database="flytau_db",
            autocommit=False
        )
        cursor = mydb.cursor()

        # 1) Verify booking belongs to this customer
        cursor.execute(
            "SELECT 1 FROM Booking WHERE B_ID = %s AND Client_Email = %s LIMIT 1",
            (booking_id, email)
        )
        if cursor.fetchone() is None:
            mydb.rollback()
            return abort(403)



        # 1.5) Check for 36-hour cancellation policy using DB time
        # If the flight is within 36 hours from NOW(), we find a row -> Block it.
        cursor.execute("""
            SELECT 1
            FROM Flight_Ticket T
            JOIN Flight F ON T.F_ID = F.F_ID
            WHERE T.B_ID = %s
              AND TIMESTAMP(F.Date_of_flight, F.Time_of_flight) < DATE_ADD(NOW(), INTERVAL 36 HOUR)
            LIMIT 1
        """, (booking_id,))
        
        if cursor.fetchone():
            mydb.rollback()
            flash("Error: You can only cancel a flight at least 36 hours before departure.", "error")
            return redirect(url_for("my_bookings"))

        # 2) Delete tickets (this releases seats)
        cursor.execute("DELETE FROM Flight_Ticket WHERE B_ID = %s", (booking_id,))

        # 3) Delete booking itself
        cursor.execute("DELETE FROM Booking WHERE B_ID = %s", (booking_id,))

        mydb.commit()
        return redirect(url_for("my_bookings"))

    except mysql.connector.Error as err:
        if mydb:
            mydb.rollback()
        return abort(500, description=f"Database error: {err}")

    finally:
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()



@app.route("/manager/flights")
@login_required(role="manager")
def manager_flights():
    """
    מנהל רואה את כל הטיסות + אפשרות סינון לפי סטטוס:
    Active / Full / Completed / Cancelled
    """
    status_filter = (request.args.get("status") or "All").strip()

    query = """
        SELECT
            f.F_ID,
            f.Status,
            f.Type,
            f.Date_of_flight,
            f.Time_of_flight,
            f.Date_of_Arrival,
            f.Time_of_Arrival,
            r.Airport_Name_Source,
            r.Airport_Name_Dest,
            (SELECT COUNT(*) FROM Seat s WHERE s.A_ID = f.A_ID) AS total_seats,
            (SELECT COUNT(*) FROM Flight_Ticket t WHERE t.F_ID = f.F_ID) AS booked_seats
        FROM Flight f
        JOIN Route r ON r.R_ID = f.R_ID
        ORDER BY f.Date_of_flight DESC, f.Time_of_flight DESC
    """

    with db_curr() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    now = datetime.now()
    flights = []

    for r in rows:
        total_seats = r[9] or 0
        booked_seats = r[10] or 0
        seats_left = max(total_seats - booked_seats, 0)

        flight_time = _mysql_time_to_timeobj(r[4])
        flight_dt = datetime.combine(r[3], flight_time)

        # סטטוס "מחושב" לפי דרישות ההנחיה
        if (r[1] or "").lower() == "cancelled":
            computed = "Cancelled"
        elif flight_dt < now:
            computed = "Completed"
        elif seats_left == 0:
            computed = "Full"
        else:
            computed = "Active"

        item = {
            "F_ID": r[0],
            "db_status": r[1],
            "Type": r[2],
            "Date_of_flight": r[3],
            "Time_of_flight": flight_time,
            "Date_of_Arrival": r[5],
            "Time_of_Arrival": _mysql_time_to_timeobj(r[6]),
            "Source": r[7],
            "Dest": r[8],
            "total_seats": total_seats,
            "booked_seats": booked_seats,
            "seats_left": seats_left,
            "computed_status": computed,
        }

        if status_filter == "All" or status_filter == computed:
            flights.append(item)

    return render_template("manager_flights.html", flights=flights, status_filter=status_filter)


@app.route("/manager/flights/add", methods=["GET", "POST"])
@login_required(role="manager")
def manager_add_flight():

    def load_dropdowns():
        with db_curr() as cursor:
            cursor.execute("SELECT A_ID, Size FROM Airplane ORDER BY A_ID")
            airplanes_local = cursor.fetchall()

            cursor.execute("""
                SELECT R_ID, Airport_Name_Source, Airport_Name_Dest, Flight_Duration
                FROM Route
                ORDER BY R_ID
            """)
            routes_local = cursor.fetchall()

        return airplanes_local, routes_local

    # ---------- GET ----------
    if request.method == "GET":
        airplanes, routes = load_dropdowns()
        return render_template("manager_add_flight.html", airplanes=airplanes, routes=routes)

    # ---------- POST ----------
    stage = (request.form.get("stage") or "").strip()  # "" / "confirm"

    a_id = request.form.get("a_id", type=int)
    r_id = request.form.get("r_id", type=int)
    date_f = request.form.get("date_f")   # YYYY-MM-DD
    time_f = request.form.get("time_f")   # HH:MM

    regular_price = request.form.get("regular_price", type=float)
    business_price = request.form.get("business_price", type=float)

    airplanes, routes = load_dropdowns()

    if not all([a_id, r_id, date_f, time_f, regular_price is not None, business_price is not None]):
        return render_template("manager_add_flight.html", airplanes=airplanes, routes=routes,
                               error="Please fill all fields (including prices).")

    # parse departure datetime
    try:
        departure_dt = datetime.strptime(f"{date_f} {time_f}", "%Y-%m-%d %H:%M")
    except ValueError:
        return render_template("manager_add_flight.html", airplanes=airplanes, routes=routes,
                               error="Invalid date/time format.")

    with db_curr() as cursor:
        # 1) airplane size
        cursor.execute("SELECT Size FROM Airplane WHERE A_ID = %s", (a_id,))
        arow = cursor.fetchone()
        if not arow:
            return render_template("manager_add_flight.html", airplanes=airplanes, routes=routes,
                                   error="Invalid airplane selected.")
        airplane_size = (arow[0] or "").strip().lower()

        # 2) route duration
        cursor.execute("SELECT Flight_Duration FROM Route WHERE R_ID = %s", (r_id,))
        rrow = cursor.fetchone()
        if not rrow or rrow[0] is None:
            return render_template("manager_add_flight.html", airplanes=airplanes, routes=routes,
                                   error="Route Flight_Duration is missing.")
        duration_hours = int(rrow[0])

        # rule: small airplane -> only routes under 6 hours
        if airplane_size == "small" and duration_hours >= 6:
            return render_template("manager_add_flight.html", airplanes=airplanes, routes=routes,
                                   error="Small airplanes can only be assigned to routes under 6 hours.")

        # Type auto by duration
        f_type = "Short" if duration_hours < 6 else "Long"

        # arrival auto by duration
        arrival_dt = departure_dt + timedelta(hours=duration_hours)
        date_a = arrival_dt.date().isoformat()
        time_a = arrival_dt.time().strftime("%H:%M:%S")

        # requirements: Large->3 pilots + 6 attendants ; Small->2 pilots + 3 attendants
        if airplane_size == "large":
            req_pilots, req_attendants = 3, 6
        else:
            req_pilots, req_attendants = 2, 3

        new_dep_str = departure_dt.strftime("%Y-%m-%d %H:%M:%S")
        new_arr_str = arrival_dt.strftime("%Y-%m-%d %H:%M:%S")

        # pilots available: trained if long + not busy in overlapping flight
        pilot_query = """
        SELECT e.E_ID, e.FirstName, e.LastName
        FROM Pilot p
        JOIN Employee e ON e.E_ID = p.E_ID
        WHERE
          (%s = 'short' OR LOWER(p.Training_for_long_flights) = 'yes')
          AND NOT EXISTS (
            SELECT 1
            FROM Flight_Crew fc
            JOIN Flight f ON f.F_ID = fc.F_ID
            WHERE fc.E_ID = e.E_ID
              AND LOWER(f.Status) <> 'cancelled'
              AND TIMESTAMP(f.Date_of_flight, f.Time_of_flight) < %s
              AND TIMESTAMP(f.Date_of_Arrival, f.Time_of_Arrival) > %s
          )
        ORDER BY e.E_ID
        """
        cursor.execute(pilot_query, (f_type.lower(), new_arr_str, new_dep_str))
        available_pilots = cursor.fetchall()

        # attendants available: trained if long + not busy in overlapping flight
        att_query = """
        SELECT e.E_ID, e.FirstName, e.LastName
        FROM Flight_Attendant fa
        JOIN Employee e ON e.E_ID = fa.E_ID
        WHERE
          (%s = 'short' OR LOWER(fa.Training_for_long_flights) = 'yes')
          AND NOT EXISTS (
            SELECT 1
            FROM Flight_Crew fc
            JOIN Flight f ON f.F_ID = fc.F_ID
            WHERE fc.E_ID = e.E_ID
              AND LOWER(f.Status) <> 'cancelled'
              AND TIMESTAMP(f.Date_of_flight, f.Time_of_flight) < %s
              AND TIMESTAMP(f.Date_of_Arrival, f.Time_of_Arrival) > %s
          )
        ORDER BY e.E_ID
        """
        cursor.execute(att_query, (f_type.lower(), new_arr_str, new_dep_str))
        available_attendants = cursor.fetchall()

        # required by guidelines: if not enough crew -> show message and stop
        if len(available_pilots) < req_pilots or len(available_attendants) < req_attendants:
            return render_template(
                "manager_add_flight.html",
                airplanes=airplanes,
                routes=routes,
                error=(
                    f"This flight cannot be published: not enough available crew for the selected time. "
                    f"(Need {req_pilots} pilots and {req_attendants} attendants)"
                )
            )

        # ---------- STAGE: show crew selection ----------
        if stage != "confirm":
            return render_template(
                "manager_add_flight_crew.html",
                a_id=a_id,
                r_id=r_id,
                date_f=date_f,
                time_f=time_f,
                date_a=date_a,
                time_a=time_a,
                duration_hours=duration_hours,
                airplane_size=airplane_size,
                f_type=f_type,
                req_pilots=req_pilots,
                req_attendants=req_attendants,
                available_pilots=available_pilots,
                available_attendants=available_attendants,
                # ✅ keep prices for confirm stage
                regular_price=regular_price,
                business_price=business_price
            )

        # ---------- STAGE: confirm (create flight + crew) ----------
        selected_pilots = request.form.getlist("pilots")
        selected_attendants = request.form.getlist("attendants")

        if len(selected_pilots) != req_pilots:
            return render_template(
                "manager_add_flight_crew.html",
                error=f"Please select exactly {req_pilots} pilot(s).",
                a_id=a_id, r_id=r_id, date_f=date_f, time_f=time_f,
                date_a=date_a, time_a=time_a, duration_hours=duration_hours,
                airplane_size=airplane_size, f_type=f_type,
                req_pilots=req_pilots, req_attendants=req_attendants,
                available_pilots=available_pilots,
                available_attendants=available_attendants,
                regular_price=regular_price,
                business_price=business_price
            )

        if len(selected_attendants) != req_attendants:
            return render_template(
                "manager_add_flight_crew.html",
                error=f"Please select exactly {req_attendants} attendant(s).",
                a_id=a_id, r_id=r_id, date_f=date_f, time_f=time_f,
                date_a=date_a, time_a=time_a, duration_hours=duration_hours,
                airplane_size=airplane_size, f_type=f_type,
                req_pilots=req_pilots, req_attendants=req_attendants,
                available_pilots=available_pilots,
                available_attendants=available_attendants,
                regular_price=regular_price,
                business_price=business_price
            )

        # last safety: prevent duplicates inside selection
        if len(set(selected_pilots)) != len(selected_pilots) or len(set(selected_attendants)) != len(selected_attendants):
            return render_template(
                "manager_add_flight_crew.html",
                error="Duplicate crew selection detected.",
                a_id=a_id, r_id=r_id, date_f=date_f, time_f=time_f,
                date_a=date_a, time_a=time_a, duration_hours=duration_hours,
                airplane_size=airplane_size, f_type=f_type,
                req_pilots=req_pilots, req_attendants=req_attendants,
                available_pilots=available_pilots,
                available_attendants=available_attendants,
                regular_price=regular_price,
                business_price=business_price
            )

        # insert flight
        new_f_id = next_id(cursor, "Flight", "F_ID")
        cursor.execute("""
            INSERT INTO Flight
            (F_ID, Status, Type, Date_of_flight, Time_of_flight,
             Date_of_Arrival, Time_of_Arrival, A_ID, R_ID,
             regular_ticket_price, business_ticket_price)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (new_f_id, "Active", f_type, date_f, time_f, date_a, time_a, a_id, r_id,
              regular_price, business_price))

        # insert crew assignments
        for e_id in selected_pilots:
            cursor.execute(
                "INSERT INTO Flight_Crew (E_ID, F_ID, Duty) VALUES (%s, %s, %s)",
                (int(e_id), new_f_id, "Pilot")
            )

        for e_id in selected_attendants:
            cursor.execute(
                "INSERT INTO Flight_Crew (E_ID, F_ID, Duty) VALUES (%s, %s, %s)",
                (int(e_id), new_f_id, "Attendant")
            )

    return redirect(url_for("manager_flights"))


@app.route("/manager/crew/add", methods=["GET", "POST"])
@login_required(role="manager")
def manager_add_crew():
    """
    הוספת אנשי צוות.
    הערה: מאחר ובקבצים שהעלית אין את סכמת Employee/Pilot/Attendant המלאה,
    ייתכן שתצטרכי להתאים שמות טבלאות/עמודות.
    """
    if request.method == "GET":
        return render_template("manager_add_crew.html")

    role = (request.form.get("role") or "").strip()  # Pilot / Attendant
    e_id = request.form.get("e_id", type=int)
    first = (request.form.get("first_name") or "").strip()
    last = (request.form.get("last_name") or "").strip()

    if not all([role, e_id, first, last]):
        return render_template("manager_add_crew.html", error="Please fill all fields.")

    with db_curr() as cursor:
        # מינימום: Employee(E_ID, FirstName, LastName) - תתאימי אם יש עוד שדות חובה
        cursor.execute("""
            INSERT INTO Employee (E_ID, FirstName, LastName)
            VALUES (%s, %s, %s)
        """, (e_id, first, last))

        # טבלאות תפקיד (ייתכן שהשמות אצלכם שונים)
        if role.lower() == "pilot":
            cursor.execute("INSERT INTO Pilot (E_ID) VALUES (%s)", (e_id,))
        elif role.lower() == "attendant":
            cursor.execute("INSERT INTO Attendant (E_ID) VALUES (%s)", (e_id,))
        else:
            return render_template("manager_add_crew.html", error="Role must be Pilot or Attendant.")

    return redirect(url_for("manager"))

@app.route("/manager/flights/cancel/<int:flight_id>", methods=["POST"])
@login_required(role="manager")
def manager_cancel_flight(flight_id):
    """
    Cancel flight only up to 72 hours before.
    When cancelled: all active bookings on that flight get full refund => Booking.Price = 0.
    """
    with db_curr() as cursor:
        cursor.execute(
            "SELECT Date_of_flight, Time_of_flight, Status FROM Flight WHERE F_ID=%s LIMIT 1",
            (flight_id,)
        )
        row = cursor.fetchone()

        if not row:
            return abort(404)

        flight_date = row[0]
        flight_time = _mysql_time_to_timeobj(row[1])
        flight_status = (row[2] or "")

        flight_dt = datetime.combine(flight_date, flight_time)
        if flight_dt < datetime.now() + timedelta(hours=72):
            return abort(400, description="Managers can cancel only up to 72 hours before the flight.")

        if flight_status.lower() == "cancelled":
            return redirect(url_for("manager_flights"))

        # 1) update flight status
        cursor.execute("UPDATE Flight SET Status='Cancelled' WHERE F_ID=%s", (flight_id,))

        # 2) cancel tickets (optional but logical)
        cursor.execute("UPDATE Flight_Ticket SET Status='Cancelled' WHERE F_ID=%s", (flight_id,))

        # 3) refund bookings => Price = 0 AND Status = Cancelled
        cursor.execute("""
            UPDATE Booking
            SET Price = 0, Status = 'Cancelled'
            WHERE B_ID IN (
                SELECT DISTINCT B_ID
                FROM Flight_Ticket
                WHERE F_ID = %s
            )
        """, (flight_id,))

    return redirect(url_for("manager_flights"))


@app.route("/manager/flights/<int:flight_id>/crew")
@login_required(role="manager")
def manager_flight_crew(flight_id):
    query = """
        SELECT
            e.E_ID,
            e.FirstName,
            e.LastName,
            fc.Duty
        FROM Flight_Crew fc
        JOIN Employee e ON e.E_ID = fc.E_ID
        WHERE fc.F_ID = %s
        ORDER BY
            CASE
              WHEN LOWER(fc.Duty) = 'pilot' THEN 1
              WHEN LOWER(fc.Duty) = 'attendant' THEN 2
              ELSE 3
            END,
            e.E_ID
    """

    with db_curr() as cursor:
        cursor.execute(query, (flight_id,))
        crew_rows = cursor.fetchall()

    crew = [
        {"E_ID": r[0], "FirstName": r[1], "LastName": r[2], "Duty": r[3]}
        for r in crew_rows
    ]

    return render_template("manager_flight_crew.html", flight_id=flight_id, crew=crew)

@app.route("/manager/reports")
@login_required(role="manager")
def manager_reports():
    # --- Queries (updated / safer) ---
    q_avg_occupancy = """
    SELECT AVG(Occupancy_Rate) * 100 AS Average_Occupancy_Percentage
    FROM (
        SELECT 
            f.F_ID,
            1.0 * (SELECT COUNT(*) FROM Flight_Ticket ft WHERE ft.F_ID = f.F_ID) /
            NULLIF((SELECT COUNT(*) FROM Seat s WHERE s.A_ID = f.A_ID), 0) AS Occupancy_Rate
        FROM Flight f
        WHERE 
            f.Date_of_Arrival < CURRENT_DATE
            OR (f.Date_of_Arrival = CURRENT_DATE AND f.Time_of_Arrival < CURRENT_TIME)
    ) AS Flight_Stats;
    """

    # Revenue by plane size/manufacturer/class using ticket prices from Flight
    q_revenue_by_airplane_class = """
    SELECT 
        a.Size AS Airplane_Size,
        a.Manufacturer,
        ft.Seat_Class_Type AS Class_Type,
        SUM(
          CASE 
            WHEN LOWER(ft.Seat_Class_Type) = 'business' THEN f.business_ticket_price
            ELSE f.regular_ticket_price
          END
        ) AS Total_Revenue
    FROM Airplane a
    JOIN Flight f ON a.A_ID = f.A_ID
    JOIN Flight_Ticket ft ON f.F_ID = ft.F_ID
    WHERE ft.Status <> 'Cancelled'
    GROUP BY a.Size, a.Manufacturer, ft.Seat_Class_Type
    ORDER BY a.Size, a.Manufacturer, ft.Seat_Class_Type;
    """

    q_employee_hours = """
    SELECT 
        e.FirstName, 
        e.LastName,
        CASE 
            WHEN r.Flight_Duration >= 6 THEN 'Long Flight'
            ELSE 'Short Flight'
        END AS Flight_Category,
        SUM(r.Flight_Duration) AS Total_Flight_Hours
    FROM Employee e
    JOIN Flight_Crew fc ON e.E_ID = fc.E_ID
    JOIN Flight f       ON fc.F_ID = f.F_ID
    JOIN Route r        ON f.R_ID = r.R_ID
    WHERE f.Status <> 'Cancelled'
    GROUP BY e.E_ID, e.FirstName, e.LastName, Flight_Category
    ORDER BY e.FirstName, e.LastName;
    """

    # Monthly cancellation rate (works only if you store cancelled bookings in Booking.Status)
    q_cancellation_rate = """
    SELECT 
        YEAR(b.booking_date) AS Year,
        MONTH(b.booking_date) AS Month,
        COUNT(DISTINCT b.B_ID) AS Total_Bookings,
        SUM(CASE WHEN LOWER(b.Status) LIKE '%cancel%' THEN 1 ELSE 0 END) AS Customer_Canceled_Bookings,
        (SUM(CASE WHEN LOWER(b.Status) LIKE '%cancel%' THEN 1 ELSE 0 END) * 100.0) / COUNT(DISTINCT b.B_ID) AS Cancellation_Rate_Percentage
    FROM Booking b
    GROUP BY Year, Month
    ORDER BY Year ASC, Month ASC;
    """

    # Monthly activity per airplane + dominant route (MySQL 8+)
    q_monthly_airplane_activity = """
    WITH MonthlyBasicStats AS (
        SELECT 
            A_ID,
            YEAR(Date_of_flight) AS Flight_Year,
            MONTH(Date_of_flight) AS Flight_Month,
            SUM(CASE WHEN Status <> 'Cancelled' THEN 1 ELSE 0 END) AS Performed_Flights,
            SUM(CASE WHEN Status = 'Cancelled' THEN 1 ELSE 0 END) AS Cancelled_Flights,
            COUNT(DISTINCT CASE WHEN Status <> 'Cancelled' THEN Date_of_flight END) / 30.0 AS Utilization_Rate
        FROM Flight
        GROUP BY A_ID, Flight_Year, Flight_Month
    ),
    RouteFrequency AS (
        SELECT 
            A_ID,
            YEAR(Date_of_flight) AS Flight_Year,
            MONTH(Date_of_flight) AS Flight_Month,
            R_ID,
            ROW_NUMBER() OVER (
                PARTITION BY A_ID, YEAR(Date_of_flight), MONTH(Date_of_flight)
                ORDER BY COUNT(*) DESC
            ) AS Route_Rank
        FROM Flight
        WHERE Status <> 'Cancelled'
        GROUP BY A_ID, Flight_Year, Flight_Month, R_ID
    )
    SELECT 
        ms.A_ID,
        ms.Flight_Year,
        ms.Flight_Month,
        ms.Performed_Flights AS Num_Flights_Performed,
        ms.Cancelled_Flights AS Num_Flights_Cancelled,
        ms.Utilization_Rate AS Monthly_Utilization,
        CONCAT(r.Airport_Name_Source, ' -> ', r.Airport_Name_Dest) AS Dominant_Route
    FROM MonthlyBasicStats ms
    LEFT JOIN RouteFrequency rf ON ms.A_ID = rf.A_ID 
        AND ms.Flight_Year = rf.Flight_Year 
        AND ms.Flight_Month = rf.Flight_Month 
        AND rf.Route_Rank = 1
    LEFT JOIN Route r ON rf.R_ID = r.R_ID
    ORDER BY ms.Flight_Year DESC, ms.Flight_Month DESC, ms.A_ID;
    """

    with db_curr() as cursor:
        cursor.execute(q_avg_occupancy)
        avg_occ_row = cursor.fetchone()
        avg_occupancy = float(avg_occ_row[0]) if avg_occ_row and avg_occ_row[0] is not None else 0.0

        cursor.execute(q_revenue_by_airplane_class)
        revenue_rows = cursor.fetchall()

        cursor.execute(q_employee_hours)
        emp_rows = cursor.fetchall()

        cursor.execute(q_cancellation_rate)
        cancel_rows = cursor.fetchall()

        cursor.execute(q_monthly_airplane_activity)
        activity_rows = cursor.fetchall()

    # --- Shape data for template ---
    revenue = [
        {"Airplane_Size": r[0], "Manufacturer": r[1], "Class_Type": r[2], "Total_Revenue": float(r[3] or 0)}
        for r in revenue_rows
    ]

    employee_hours = [
        {"FirstName": r[0], "LastName": r[1], "Category": r[2], "Hours": float(r[3] or 0)}
        for r in emp_rows
    ]

    cancellation = [
        {"Year": int(r[0]), "Month": int(r[1]), "Total": int(r[2] or 0),
         "Canceled": int(r[3] or 0), "Rate": float(r[4] or 0)}
        for r in cancel_rows
    ]

    airplane_activity = [
        {"A_ID": int(r[0]), "Year": int(r[1]), "Month": int(r[2]),
         "Performed": int(r[3] or 0), "Cancelled": int(r[4] or 0),
         "Utilization": float(r[5] or 0), "DominantRoute": r[6] or ""}
        for r in activity_rows
    ]

    return render_template(
        "manager_reports.html",
        avg_occupancy=avg_occupancy,
        revenue=revenue,
        employee_hours=employee_hours,
        cancellation=cancellation,
        airplane_activity=airplane_activity
    )

@app.route('/booking-review', methods=['POST'])
def booking_review_page():
    flight_id = request.form.get("flight_id")
    seats = request.form.getlist("seats")

    if not flight_id or not seats:
        return redirect(url_for("search"))

    seat_data = []
    total_price = 0.0

    econ_count = 0
    bus_count = 0

    with db_curr() as cursor:
        cursor.execute("""
            SELECT regular_ticket_price, business_ticket_price
            FROM Flight
            WHERE F_ID = %s
        """, (flight_id,))
        flight = cursor.fetchone()

        regular_price = float(flight[0])
        business_price = float(flight[1])

        for seat in seats:
            col, row, cls = seat.split("|")
            price = business_price if cls.lower() == "business" else regular_price
            total_price += price

            if cls.lower() == "business":
                bus_count += 1
            else:
                econ_count += 1

            seat_data.append({
                "seat": f"{col}{row}",
                "class": cls,
                "price": price
            })

    cancellation_fee = total_price * 0.05

    return render_template(
        "booking_review.html",
        seats=seat_data,
        flight_id=flight_id,
        regular_price=regular_price,
        business_price=business_price,
        econ_count=econ_count,
        bus_count=bus_count,
        total=total_price,
        cancellation_fee=cancellation_fee,
        raw_seats=seats,
        num_tickets=len(seats)
    )


if __name__ == "__main__":
    app.run(debug=True)