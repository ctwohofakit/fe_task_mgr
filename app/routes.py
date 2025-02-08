from flask import (
    Flask,
    render_template,
    request as flask_request,
    redirect,
    url_for, abort,
)


import requests

app = Flask(__name__)

BACKEND_URL="http://127.0.0.1:5000/tasks"

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/about")
def about():
    return render_template("about.html")

@app.get("/newtask")
def newtask():
    return render_template("newtask.html")



@app.get("/tasks")
def task_list():
    response =requests.get(BACKEND_URL) #response = to requesting (requests)from backend
    if response.status_code==200:
        task_data=response.json().get("tasks")
        return render_template("list.html", tasks=task_data) #tasks will be the name to allow to access the "list.html"
    return(
        render_template("list.html", error=response.status_code),
        response.status_code
    )

@app.get("/tasks/<int:pk>/edit")
def edit_form(pk):
    url="%s/%s" % (BACKEND_URL, pk)
    response =requests.get(url)
    if response.status_code==200:
        single_task=response.json().get("task") #this template does not exist yet
        return render_template("edit.html", task=single_task)
    return(
        render_template("error.html", error=response.statsus_code),
        response.status_code
    )

@app.post("/tasks/<int:pk>/edit")
def edit_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.put(url, json=flask_request.form)
    if response.status_code == 204:
        return render_template("success.html", message="Task edited")
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

# @app.delete("/tasks/<int:pk>/delete")
# def delete_task(pk):
#     url = "%s/%s" % (BACKEND_URL, pk)
#     response = requests.delete(url)
#     if response.status_code == 204:
#         return redirect(url_for("task_list"))
#     return (
#         render_template("error.html", error=response.status_code),
#         response.status_code
#     )

@app.route("/tasks/<int:pk>/delete", methods=["POST", "DELETE"])
def delete_task(pk):
    if flask_request.method == "POST" and flask_request.form.get('_method') == 'DELETE':
        pass 
    elif flask_request.method == "DELETE":
        pass  

    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.delete(url)
    if response.status_code == 204:
        return redirect(url_for("task_list"))
    return render_template("error.html", error=response.status_code), response.status_code

@app.post("/tasks/create")
def create_task():
    url = BACKEND_URL
    response = requests.post(url, json=flask_request.form)#json over the dictory
    if response.status_code == 204:
        return render_template("success.html", message="Task created")
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )