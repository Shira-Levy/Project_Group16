from flask import Flask, redirect, render_template, request, session, url_for
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

Session(app)wdqw

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



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login_form.html')

    # Customer (Registered)
    customer_email = request.form.get("customer_email")
    customer_password = request.form.get("customer_password")

    # Manager (Manger)
    manager_id = request.form.get("manager_id")
    manager_password = request.form.get("manager_password")

    # --- Customer login ---
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
            return render_template('login_form.html', error="Invalid customer email/password")

        session.clear()
        session["role"] = "customer"
        session["email"] = row[0]
        session["first_name"] = row[1]
        session["last_name"] = row[2]
        return redirect(url_for("home_page"))

    # --- Manager login ---
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
            return render_template('login_form.html', error="Invalid manager ID/password")

        session.clear()
        session["role"] = "manager"
        session["manager_e_id"] = row[0]
        session["first_name"] = row[1]
        session["last_name"] = row[2]
        return redirect(url_for("manager"))

    return render_template('login_form.html', error="Please fill one of the login forms.")


def login_required(role=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if "role" not in session:
                return redirect(url_for("login"))
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

    query_flight = "SELECT A_ID FROM Flight WHERE F_ID=%s LIMIT 1"

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

        cursor.execute(query_seats, (airplane_id, flight_id))
        seats = cursor.fetchall()

    seat_items = [
        {"col": s[0], "row": s[1], "class": s[2], "value": f"{s[0]}|{s[1]}|{s[2]}"}
        for s in seats
    ]

    session["last_seats"] = seat_items

    if num_tickets > len(seat_items):
        return render_template(
            "choose_seats.html",
            seats=seat_items,
            flight_id=flight_id,
            num_tickets=num_tickets,
            error=f"Only {len(seat_items)} seats are available."
        )

    return render_template(
        "choose_seats.html",
        seats=seat_items,
        flight_id=flight_id,
        num_tickets=num_tickets
    )


@app.route('/book-selected-seats', methods=['POST'])
def book_selected_seats():
    if session.get("role") != "customer":
        return redirect(url_for("login"))

    flight_id = request.form.get("flight_id")
    num_tickets = request.form.get("num_tickets", type=int)
    selected = request.form.getlist("seats")

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

    customer_email = session.get("email") or session.get("customer_email")
    if not customer_email:
        return redirect(url_for("login"))

    parsed = []
    for v in selected:
        col, row_str, class_type = v.split("|")
        parsed.append((col, int(row_str), class_type))

    with db_curr() as cursor:
        cursor.execute("SELECT A_ID FROM Flight WHERE F_ID=%s LIMIT 1", (flight_id,))
        fr = cursor.fetchone()
        if not fr:
            return redirect(url_for("search"))
        airplane_id = fr[0]

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

        for col, row_num, class_type in parsed:
            cursor.execute(check_seat_available, (airplane_id, col, row_num, class_type, flight_id))
            if not cursor.fetchone():
                return render_template("booking_success.html", error="One or more selected seats are no longer available.")

        cursor.execute("SELECT COALESCE(MAX(B_ID), 0) + 1 FROM Booking")
        booking_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO Booking (B_ID, Status, Price, Cancellation_Fee, booking_date, booking_time, Client_Email)
            VALUES (%s, %s, %s, %s, CURDATE(), CURTIME(), %s)
            """,
            (booking_id, "Confirmed", 0, 0, customer_email)
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
        return redirect(url_for("login"))

    email = session.get("email")
    if not email:
        return redirect(url_for("login"))

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
        return redirect(url_for("login"))

    email = session.get("email")
    if not email:
        return redirect(url_for("login"))

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



if __name__ == "__main__":
    app.run(debug=True)