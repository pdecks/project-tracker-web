from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def show_home():
    """Display homepage with list of students and list of projects"""
    student_rows = hackbright.get_students()
    project_rows = hackbright.get_projects()
    html = render_template("home.html",
                           student_rows=student_rows,
                           project_rows=project_rows)
    return html

@app.route("/student_info/<firstname><lastname>")
def display_student(firstname, lastname):
    """Display student info"""

    first = firstname
    print first
    last = lastname
    print last
          
    github = hackbright.get_github_by_student(first, last)
    # pass github to get_grades_by_github
    # get project/title info
    rows = hackbright.get_grades_by_github(github)
    # print "This is rows: %s" % rows
    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           rows=rows) #update to pass list

    return html

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')
    first, last, github = hackbright.get_student_by_github(github)
    # get project/title info
    rows = hackbright.get_grades_by_github(github)
    # print "This is rows: %s" % rows
    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           rows=rows) #update to pass list

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

    html = render_template("student-added.html",
                           first=first,
                           last=last,
                           github=github)

    return html

@app.route("/student-add")
def get_student_add_form():
    """Show form for adding a student."""

    return render_template("student-add.html")

@app.route("/project/<proj_title>")
def display_project(proj_title):
    """Show info for the project clicked on"""
    title, description, max_grade= hackbright.get_project_by_title(proj_title)
    rows= hackbright.get_names_and_grades_by_title(title) # replace with new function that return student name and grade
    return render_template("project.html",
                           title=title,
                           description=description,
                           max_grade=max_grade,
                           rows=rows)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
