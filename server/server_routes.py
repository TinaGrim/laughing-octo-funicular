from flask import Flask, jsonify , request, url_for, render_template, blueprints

grim = blueprints.Blueprint('grim', __name__)
RemainingID = []
LDActivity_data = {}
GUI = None

@grim.route("/schedule")
def scheduleFunc():
    if GUI is None:
        return jsonify(scheduleClose=True)
    
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify(template="schedule.html", scheduleClose=GUI.scheduleClose)
    
    return render_template("schedule.html", scheduleClose=GUI.scheduleClose)

@grim.route("/LDActivity", methods=["GET", "POST"])
def LDActivity():
    if GUI is None:
        return jsonify(LDActivity=[])

    if request.method == "POST":
        data = request.get_json()

        for key in data.keys():
            LDActivity_data[key] = data[key]
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify(LDActivity=LDActivity_data)
        return render_template("LDActivity.html", LDActivity=data)
    elif request.method == "GET":
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify(LDActivity=LDActivity_data)
        return render_template("LDActivity.html", LDActivity=LDActivity_data)
    else:
        return render_template("LDActivity.html", LDActivity=[])


@grim.route("/Order", methods=["GET", "POST"])
def Order():
    if GUI is None:
        return jsonify(Order=[])
    
    for btn in GUI.LD_Button_list_qp.buttons():
        btn.setChecked(False)
    
    # if request.method == "POST":
        
    #     ID = request.get_json()
    #     RemainingID.clear()
    #     RemainingID.extend(ID)
        
        
    #     print("[ \033[92mOK\033[0m ] " + "RemainingID after POST: ", RemainingID)
        
    #     return render_template("Order.html", Order=RemainingID)
    if request.method == "POST":
        ID = request.get_json()
        RemainingID.clear()
        RemainingID.extend(ID)
        
        if request.headers.get('Content-Type') == 'application/json':
            print("[ \033[92mOK\033[0m ] " + "RemainingID after POST: ", RemainingID)
            return jsonify(Order=RemainingID)
        return render_template("Order.html", Order=RemainingID)
    elif request.method == "GET":
        if request.headers.get('Content-Type') == 'application/json':
            print("[ \033[92mOK\033[0m ] " + "RemainingID after GET: ", RemainingID)
            return jsonify(Order=RemainingID)
        return render_template("Order.html", Order=RemainingID)
    else:
        return render_template("Order.html", Order=[])

@grim.route("/DevicesList")
def DevicesList():
    if GUI is None:
        return jsonify(DevicesList=[])
    
    devices = GUI.Grim.check_ld_in_list()
    if request.headers.get('Content-Type') == 'application/json':
        print("[ \033[92mOK\033[0m ] " + "DevicesList: ", devices)
        return jsonify(DevicesList=devices)
    
    return render_template("DevicesList.html", DevicesList=devices)

def init(server, window):
    global GUI
    GUI = window
    server.register_blueprint(grim)