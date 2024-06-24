import sqlite3

from flask import Flask, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True



@app.route("/", methods=["GET", "POST"])
def index():
	
	if request.method == "POST":

		# TODO: request all fields from the HTML form (opponent, day, month, location)
		opponent = request.form.get('opponent')
		month = request.form.get('month')
		day = request.form.get('day')
		location = request.form.get('location')
		print("oppenent=" + str(opponent))
		print("month=" + str(month))

		# TODO: create a SQL statement to INSERT event into the database
		con = sqlite3.connect('events.db')
		cur = con.cursor()
		query = "INSERT INTO events (opponent, day, month, location) VALUES('"+opponent +"','"+day +"', '"+month+"', '"+location+"')"
		print(query)
		cur.execute(query)
		con.commit()
		con.close()
		return redirect("/")
		
	elif request.args.get("id",default="") != "":
		eventid = request.args.get("id")

		# TODO: get the id from the query string

		# Connect to database and delete event from the database using the event id
		con = sqlite3.connect('events.db')
		cur = con.cursor()
		query = "DELETE FROM events WHERE id='"+eventid+"'"
		print(query)
		cur.execute(query)
		con.commit()
		con.close()
		return redirect("/")

	else:

		# TODO: Query the database events.db and select all records from event table
		with sqlite3.connect('events.db') as conn:
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor()
			cursor.execute("SELECT id, opponent, day, month, location FROM events ORDER BY month, day")
			events_rows = (cursor.fetchall())
		# TODO: add a parameter pass events to the HTML template
		return render_template("index.html", events=events_rows)



app.run(host='0.0.0.0', port=8080)