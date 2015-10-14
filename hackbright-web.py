from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')
    first, last, github = hackbright.get_student_by_github(github)
    # get project/title info
    rows = hackbright.get_grades_by_github(github)
    # print "This is rows: %s" % rows
    html = render_template("student_info.html", first=first, last=last, github=github, rows=rows) #update to pass list

    return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-added", methods=['POST'])
def student_add():
    """Add a student."""
    github = request.form.get('github')
    first = request.form.get('firstname')
    last = request.form.get('lastname')
    # print "This is github: %s" % github
    # print "This is firstname: %s" % fname
    # print "This is lastname: %s" % lname
    hackbright.make_new_student(first, last, github)
    html = render_template("student-added.html", first=first, last=last, github=github)

    return html

@app.route("/student-add")
def get_student_add_form():
    """Show form for adding a student."""

    return render_template("student-add.html")

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
