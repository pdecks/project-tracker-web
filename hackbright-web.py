from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')
    first, last, github = hackbright.get_student_by_github(github)
    html = render_template("student_info.html", first=first, last=last, github=github)

    return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-added", methods=['POST'])
def student_add():
    """Add a student."""
    github = request.form.get('github')
    fname = request.form.get('firstname')
    lname = request.form.get('lastname')
    fname, lname, github = hackbright.make_new_student(fname, lname, github)
    html = render_template("student-added.html", fname=fname, lname=lname, github=github)

    return html

@app.route("/student-add")
def get_student_add_form():
    """Show form for adding a student."""

    return render_template("student-add.html")

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
