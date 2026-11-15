from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = "secret123"

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'house_app'

mysql = MySQL(app)



UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ---------------- INDEX ----------------
@app.route('/')
def index():
    return render_template('index.html')

# ---------------- OWNER REGISTER ----------------
@app.route('/owner/register', methods=['GET', 'POST'])
def owner_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        location = request.form['location']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO owners (name, email, mobile, password, location)
            VALUES (%s,%s,%s,%s,%s)
        """, (name, email, mobile, password, location))
        mysql.connection.commit()
        cur.close()
        return redirect('/owner/login')

    return render_template('owner_register.html')

# ---------------- OWNER LOGIN ----------------
@app.route('/owner/login', methods=['GET', 'POST'])
def owner_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM owners WHERE email=%s AND password=%s", (email, password))
        owner = cur.fetchone()
        cur.close()

        if owner:
            session['owner'] = owner[0]
            return redirect('/owner/dashboard')

    return render_template('owner_login.html')

# ---------------- OWNER DASHBOARD ----------------
@app.route('/owner/dashboard')
def owner_dashboard():
    if 'owner' not in session:
        return redirect('/owner/login')
    return render_template('owner_dashboard.html')


@app.route('/owner/add-house', methods=['GET', 'POST'])
def add_house():
    if 'owner' not in session:
        return redirect('/owner/login')

    if request.method == 'POST':
        owner_id = session['owner']

        flat_number = request.form['flat_number']
        flat_name = request.form['flat_name']  # NEW FIELD
        area_name = request.form['area_name']
        location = request.form['location']
        pincode = request.form['pincode']
        rent_per_month = request.form['rent_per_month']
        advance = request.form['advance']
        no_of_rooms = request.form['no_of_rooms']
        no_of_bedrooms = request.form['no_of_bedrooms']

        images = []
        for i in range(1, 6):
            file = request.files.get(f'image{i}')
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                images.append(filename)
            else:
                images.append(None)

        cur = mysql.connection.cursor()
        cur.execute("""
    INSERT INTO houses 
    (owner_id, flat_number, flat_name, area_name, location, pincode,
     rent_per_month, advance, no_of_rooms, no_of_bedrooms,
     image1, image2, image3, image4, image5)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
""", (
    owner_id, flat_number, flat_name, area_name, location, pincode,
    rent_per_month, advance, no_of_rooms, no_of_bedrooms,
    images[0], images[1], images[2], images[3], images[4]
))


        mysql.connection.commit()
        cur.close()
        return redirect('/owner/view-houses')

    return render_template('add_house.html')





# VIEW HOUSES
@app.route('/owner/view-houses')
def view_houses():
    if 'owner' not in session:
        return redirect('/owner/login')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM houses WHERE owner_id=%s", (session['owner'],))
    houses = cur.fetchall()
    cur.close()
    return render_template('view_houses.html', houses=houses)

# DELETE HOUSE
@app.route('/owner/delete-house/<int:id>')
def delete_house(id):
    if 'owner' not in session:
        return redirect('/owner/login')
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM houses WHERE house_id=%s AND owner_id=%s", (id, session['owner']))
    mysql.connection.commit()
    cur.close()
    return redirect('/owner/view-houses')

# GET HOUSE DATA (AJAX)
@app.route('/owner/get-house/<int:house_id>')
def get_house(house_id):
    if 'owner' not in session:
        return {"error": "Unauthorized"}, 401

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 
            house_id,
            flat_number,
            flat_name,
            area_name,
            location,
            pincode,
            rent_per_month,
            advance,
            no_of_rooms,
            no_of_bedrooms,
            image1, image2, image3, image4, image5
        FROM houses
        WHERE house_id=%s AND owner_id=%s
    """, (house_id, session['owner']))

    row = cur.fetchone()
    cur.close()

    if not row:
        return {"error": "House not found"}, 404

    return {
        "house_id": row[0],
        "flat": row[1],
        "flat_name": row[2],   # ✅ FIXED
        "area": row[3],
        "location": row[4],
        "pincode": row[5],
        "rent": row[6],
        "advance": row[7],
        "rooms": row[8],
        "bedrooms": row[9],
        "images": row[10:15]
    }

# EDIT HOUSE
@app.route('/owner/edit-house', methods=['POST'])
def edit_house():
    if 'owner' not in session:
        return redirect('/owner/login')

    house_id = request.form['house_id']
    flat = request.form['flat']
    flat_name = request.form.get('flat_name')  # NEW
    area = request.form['area']
    location = request.form['location']
    pincode = request.form['pincode']
    rent = request.form['rent']
    advance = request.form['advance']
    rooms = request.form['rooms']
    bedrooms = request.form['bedrooms']

    cur = mysql.connection.cursor()
    # UPDATE TEXT FIELDS
    cur.execute("""
        UPDATE houses SET
        flat_number=%s,
        area_name=%s,
        location=%s,
        pincode=%s,
        rent_per_month=%s,
        advance=%s,
        no_of_rooms=%s,
        no_of_bedrooms=%s
        WHERE house_id=%s AND owner_id=%s
    """, (flat, area, location, pincode, rent, advance, rooms, bedrooms, house_id, session['owner']))

    # UPDATE IMAGES
    for i in range(1,6):
        file = request.files.get(f'image{i}')
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cur.execute(f"UPDATE houses SET image{i}=%s WHERE house_id=%s", (filename, house_id))

    mysql.connection.commit()
    cur.close()
    return redirect('/owner/view-houses')



@app.route('/owner/contact-responses')
def owner_contact_responses():
    if 'owner' not in session:
        return redirect('/owner/login')

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 
            c.contact_id,
            u.name,
            u.mobile,
            h.flat_number,
            c.info,
            c.queries,
            c.created_at
        FROM contacts c
        JOIN users u ON c.user_id = u.user_id
        JOIN houses h ON c.house_id = h.house_id
        WHERE h.owner_id = %s
        ORDER BY c.created_at DESC
    """, (session['owner'],))
    contacts = cur.fetchall()
    cur.close()

    return render_template('owner_contact_responses.html', contacts=contacts)


@app.route('/owner/booking-responses')
def owner_booking_responses():
    if 'owner' not in session:
        return redirect('/owner/login')

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 
            b.booking_id,
            u.name,
            h.flat_number,
            b.date_from,
            b.date_to,
            b.status,
            b.description
        FROM bookings b
        JOIN users u ON b.user_id = u.user_id
        JOIN houses h ON b.house_id = h.house_id
        WHERE b.house_owner_id = %s
        ORDER BY b.booking_date DESC
    """, (session['owner'],))
    bookings = cur.fetchall()
    cur.close()

    return render_template('owner_booking_responses.html', bookings=bookings)
  
@app.route('/owner/update-booking', methods=['POST'])
def update_booking():
    if 'owner' not in session:
        return redirect('/owner/login')

    booking_id = request.form['booking_id']
    status = request.form['status']
    description = request.form['description']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE bookings
        SET status=%s, description=%s
        WHERE booking_id=%s AND house_owner_id=%s
    """, (status, description, booking_id, session['owner']))

    mysql.connection.commit()
    cur.close()

    return redirect('/owner/booking-responses')
 
@app.route('/owner/reply-contact', methods=['POST'])
def reply_contact():
    if 'owner' not in session:
        return redirect('/owner/login')

    contact_id = request.form['contact_id']
    info_response = request.form['info_response']
    queries_response = request.form['queries_response']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE contacts
        SET info_response=%s,
            queries_response=%s
        WHERE contact_id=%s
    """, (info_response, queries_response, contact_id))

    mysql.connection.commit()
    cur.close()

    return redirect('/owner/contact-responses')

@app.route('/owner/payments')
def owner_payments():
    if 'owner' not in session:
        return redirect('/owner/login')

    owner_id = session['owner']
    cur = mysql.connection.cursor()

    # ---------------- ADVANCE PAYMENTS ----------------
    cur.execute("""
        SELECT
            ap.advance_id,
            u.name,
            h.flat_number,
            h.area_name,
            h.location,
            ap.payment_type,
            ap.reference_id,
            ap.account_number,
            ap.description,
            ap.created_at
        FROM advance_payments ap
        JOIN houses h ON ap.house_id = h.house_id
        JOIN users u ON ap.user_id = u.user_id
        WHERE h.owner_id = %s
        ORDER BY ap.created_at DESC
    """, (owner_id,))
    advance_payments = cur.fetchall()

    # ---------------- RENT PAYMENTS ----------------
    cur.execute("""
        SELECT
            rp.payment_id,
            u.name,
            h.flat_number,
            h.area_name,
            h.location,
            rp.amount,
            rp.payment_type,
            rp.reference_id,
            rp.account_number,
            rp.description,
            rp.image,
            rp.created_at
        FROM rent_payments rp
        JOIN houses h ON rp.house_id = h.house_id
        JOIN users u ON rp.user_id = u.user_id
        WHERE h.owner_id = %s
        ORDER BY rp.created_at DESC
    """, (owner_id,))
    rent_payments = cur.fetchall()

    cur.close()

    return render_template(
        'owner_payments.html',
        advance_payments=advance_payments,
        rent_payments=rent_payments
    )

  
  
  
  
@app.route('/owner/logout')
def owner_logout():
    session.pop('owner', None)   # remove owner session
    return redirect('/')

  

















# ---------------- USER REGISTER ----------------
@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        location = request.form['location']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO users (name, email, mobile, password, location)
            VALUES (%s,%s,%s,%s,%s)
        """, (name, email, mobile, password, location))
        mysql.connection.commit()
        cur.close()
        return redirect('/user/login')

    return render_template('user_register.html')

# ---------------- USER LOGIN ----------------
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            session['user'] = user[0]
            return redirect('/user/dashboard')

    return render_template('user_login.html')

# # ---------------- USER DASHBOARD ----------------
# @app.route('/user/dashboard')
# def user_dashboard():
#     if 'user' not in session:
#         return redirect('/user/login')

#     cur = mysql.connection.cursor()
#     cur.execute("""
#         SELECT 
#             h.house_id,
#             h.flat_number,
#             h.area_name,
#             h.location,
#             h.pincode,
#             h.rent_per_month,
#             h.no_of_rooms,
#             h.no_of_bedrooms,
#             h.image1,
#             o.name,
#             o.mobile
#         FROM houses h
#         JOIN owners o ON h.owner_id = o.house_owner_id
#         ORDER BY h.house_id DESC
#     """)
#     houses = cur.fetchall()
#     cur.close()

#     return render_template('user_dashboard.html', houses=houses)


# ---------------- USER DASHBOARD (NAV BAR ONLY) ----------------
@app.route('/user/dashboard')
def user_dashboard():
    if 'user' not in session:
        return redirect('/user/login')

    # No DB query here
    return render_template('user_dashboard.html')




# ---------------- USER VIEW (NEW DASHBOARD) ----------------
# @app.route('/user/view')
# def user_view():
#     if 'user' not in session:
#         return redirect('/user/login')

#     cur = mysql.connection.cursor()
#     cur.execute("""
#         SELECT 
#             h.house_id,
#             h.flat_number,
#             h.area_name,
#             h.location,
#             h.pincode,
#             h.rent_per_month,
#             h.no_of_rooms,
#             h.no_of_bedrooms,
#             h.image1,
#             o.name,
#             o.mobile
#         FROM houses h
#         JOIN owners o ON h.owner_id = o.house_owner_id
#         ORDER BY h.house_id DESC
#     """)
#     houses = cur.fetchall()
#     cur.close()

#     return render_template('user_view.html', houses=houses)

@app.route('/user/view')
def user_view():
    if 'user' not in session:
        return redirect('/user/login')

    # Get search parameters from query string
    search_area = request.args.get('search_area', '').strip()
    search_flat = request.args.get('search_flat', '').strip()
    search_location = request.args.get('search_location', '').strip()

    cur = mysql.connection.cursor()

    # Base query
    query = """
        SELECT 
            h.house_id,
            h.flat_number,
            h.flat_name,
            h.area_name,
            h.location,
            h.pincode,
            h.rent_per_month,
            h.no_of_rooms,
            h.no_of_bedrooms,
            h.image1,
            o.name,
            o.mobile
        FROM houses h
        JOIN owners o ON h.owner_id = o.house_owner_id
        WHERE 1=1
    """
    params = []

    # Add filters if provided
    if search_area:
        query += " AND h.area_name LIKE %s"
        params.append(f"%{search_area}%")
    if search_flat:
        query += " AND h.flat_name LIKE %s"
        params.append(f"%{search_flat}%")
    if search_location:
        query += " AND h.location LIKE %s"
        params.append(f"%{search_location}%")

    # Order by latest houses
    query += " ORDER BY h.house_id DESC"

    # Execute query
    cur.execute(query, params)
    houses = cur.fetchall()
    cur.close()

    return render_template(
        'user_view.html',
        houses=houses,
        search_area=search_area,
        search_flat=search_flat,
        search_location=search_location
    )


@app.route('/user/house/<int:id>')
def user_house_detail(id):
    if 'user' not in session:
        return ''

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT flat_number, area_name, location, pincode,
               rent_per_month, advance, no_of_rooms, no_of_bedrooms,
               image1, image2, image3, image4, image5
        FROM houses WHERE house_id=%s
    """, (id,))
    h = cur.fetchone()
    cur.close()

    return f"""
    <h3>House Details</h3>
    <p><b>Flat:</b> {h[0]}</p>
    <p><b>Area:</b> {h[1]}</p>
    <p><b>Location:</b> {h[2]}</p>
    <p><b>Pincode:</b> {h[3]}</p>
    <p><b>Rent:</b> ₹{h[4]}</p>
    <p><b>Advance:</b> ₹{h[5]}</p>
    <p><b>Rooms:</b> {h[6]}</p>
    <p><b>Bedrooms:</b> {h[7]}</p>
    <img src="/static/uploads/{h[8]}" width="200">
    <img src="/static/uploads/{h[9]}" width="200">
    <img src="/static/uploads/{h[10]}" width="200">
    """

@app.route('/user/contact', methods=['POST'])
def user_contact():
    if 'user' not in session:
        return redirect('/user/login')

    user_id = session['user']
    house_id = request.form['house_id']
    info = request.form['info']
    queries = request.form['queries']

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO contacts (user_id, house_id, info, queries)
        VALUES (%s,%s,%s,%s)
    """, (user_id, house_id, info, queries))
    mysql.connection.commit()
    cur.close()

    return redirect('/user/view')
 
 
# ---------------- USER BOOK HOUSE ----------------
@app.route('/user/book', methods=['POST'])
def user_book():
    if 'user' not in session:
        return redirect('/user/login')

    user_id = session['user']
    house_id = request.form['house_id']
    date_from = request.form['from_date']
    date_to = request.form.get('to_date')

    cur = mysql.connection.cursor()

    # get owner id from house
    cur.execute("SELECT owner_id FROM houses WHERE house_id=%s", (house_id,))
    owner_id = cur.fetchone()[0]

    # ✅ FIXED COLUMN NAMES
    cur.execute("""
        INSERT INTO bookings 
        (house_id, user_id, house_owner_id, date_from, date_to)
        VALUES (%s, %s, %s, %s, %s)
    """, (house_id, user_id, owner_id, date_from, date_to))

    mysql.connection.commit()
    cur.close()

    return redirect('/user/view')

 
 
 
@app.route('/user/responses')
def user_responses():
    if 'user' not in session:
        return redirect('/user/login')

    user_id = session['user']
    cur = mysql.connection.cursor()

    # Contact responses
    cur.execute("""
        SELECT 
            h.flat_number,
            h.area_name,
            h.location,
            c.info,
            c.queries,
            c.info_response,
            c.queries_response,
            c.created_at
        FROM contacts c
        JOIN houses h ON c.house_id = h.house_id
        WHERE c.user_id=%s
        ORDER BY c.created_at DESC
    """, (user_id,))
    contact_responses = cur.fetchall()

    # Booking responses **include house_id**
    cur.execute("""
        SELECT 
            b.house_id,       -- include house_id for advance payment
            h.flat_number,
            h.area_name,
            h.location,
            b.date_from,
            b.date_to,
            b.status,
            b.description,
            b.booking_date
        FROM bookings b
        JOIN houses h ON b.house_id = h.house_id
        WHERE b.user_id=%s
        ORDER BY b.booking_date DESC
    """, (user_id,))
    booking_responses = cur.fetchall()

    cur.close()
    return render_template('user_responses.html', 
                           contact_responses=contact_responses, 
                           booking_responses=booking_responses)

 
 
@app.route('/user/advance', methods=['POST'])
def user_advance():
    if 'user' not in session:
        return redirect('/user/login')

    user_id = session['user']
    house_id = request.form['house_id']
    payment_type = request.form['payment_type']
    reference_id = request.form.get('reference_id')
    account_number = request.form.get('account_number')
    description = request.form.get('description')

    # Optional: validate house_id exists
    cur = mysql.connection.cursor()
    cur.execute("SELECT house_id FROM houses WHERE house_id=%s", (house_id,))
    house = cur.fetchone()
    if not house:
        cur.close()
        return "Error: Invalid house selected"

    cur.execute("""
        INSERT INTO advance_payments
        (user_id, house_id, payment_type, reference_id, account_number, description)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (user_id, house_id, payment_type, reference_id, account_number, description))

    mysql.connection.commit()
    cur.close()
    return redirect('/user/responses')


@app.route('/user/payments')
def user_payments():
    if 'user' not in session:
        return redirect('/user/login')

    user_id = session['user']
    cur = mysql.connection.cursor()

    # Houses eligible for rent payment
    cur.execute("""
        SELECT 
            b.house_id,
            h.flat_number,
            h.area_name,
            h.location,
            h.rent_per_month
        FROM bookings b
        JOIN houses h ON b.house_id = h.house_id
        WHERE b.user_id=%s AND b.status='accepted'
    """, (user_id,))
    houses = cur.fetchall()

    # ✅ FETCH RENT PAYMENTS
    cur.execute("""
        SELECT
            rp.payment_id,
            h.flat_number,
            h.area_name,
            h.location,
            rp.amount,
            rp.payment_type,
            rp.reference_id,
            rp.account_number,
            rp.description,
            rp.image,
            rp.created_at
        FROM rent_payments rp
        JOIN houses h ON rp.house_id = h.house_id
        WHERE rp.user_id=%s
        ORDER BY rp.created_at DESC
    """, (user_id,))
    payments = cur.fetchall()

    cur.close()

    return render_template(
        'user_payments.html',
        houses=houses,
        payments=payments
    )


@app.route('/user/pay-rent', methods=['POST'])
def pay_rent():
    if 'user' not in session:
        return redirect('/user/login')

    user_id = session['user']
    house_id = request.form['house_id']
    amount = request.form['amount']
    payment_type = request.form['payment_type']
    reference_id = request.form.get('reference_id')
    account_number = request.form.get('account_number')
    description = request.form.get('description')

    image = None
    file = request.files.get('image')
    if file and file.filename:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = filename

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO rent_payments
        (user_id, house_id, amount, payment_type,
         reference_id, account_number, description, image)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (user_id, house_id, amount, payment_type,
          reference_id, account_number, description, image))

    mysql.connection.commit()
    cur.close()

    return redirect('/user/payments')


# ---------------- USER LOGOUT ----------------
@app.route('/user/logout')
def user_logout():
    session.pop('user', None)
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
