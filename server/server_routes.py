from flask import Flask, jsonify , request, url_for, render_template, blueprints

grim = blueprints.Blueprint('grim', __name__)
RemainingID = []
LDActivity_data = {}
GUI = None

@grim.route("/schedule")
def scheduleFunc():
    print("[ DEBUG ] Schedule route called")
    if GUI is None:
        return jsonify(scheduleClose=True)
    return jsonify(scheduleClose=GUI.scheduleClose)

@grim.route("/LDActivity", methods=["GET", "POST"])
def LDActivity():

    if request.method == "POST":
        data = request.get_json()

        for key in data.keys():
            LDActivity_data[key] = data[key]
        
        return jsonify(LDActivity=data)
    elif request.method == "GET":
        
        return jsonify(LDActivity=LDActivity_data)
    else:
        return jsonify(LDActivity=[])


@grim.route("/Order", methods=["GET", "POST"])
def Order():
    if GUI is None:
        return jsonify(Order=[])
    for btn in GUI.LD_Button_list_qp.buttons():
        btn.setChecked(False)
        
    if request.method == "POST":
        ID = request.get_json()
        RemainingID.clear()
        RemainingID.extend(ID)
        print("[ \033[92mOK\033[0m ] " + "RemainingID after POST: ", RemainingID)
        return jsonify(Order=RemainingID)
    elif request.method == "GET":
        return jsonify(Order=RemainingID)
    else:
        return jsonify(Order=[])

@grim.route("/DevicesList")
def DevicesList():
    if GUI is None:
        return jsonify(DevicesList=[])
    devices = GUI.Grim.check_ld_in_list()
    return jsonify(DevicesList=devices)

def init(server, window):
    global GUI
    GUI = window
    server.register_blueprint(grim)