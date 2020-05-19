import flask
from system import Reception, POSSIBLE_FIELDS


app = flask.Flask('Reception')
Reception = Reception()


@app.route('/create', methods=['POST'])
def create_reservation():
    data = {
        item: int(flask.request.form[item])
        for item in POSSIBLE_FIELDS
        if item in flask.request.form
    }

    reservation_id = Reception.create_reservation(**data)
    return str(reservation_id)


@app.route('/departure', methods=['POST'])
def departure():
    id = int(flask.request.form['id'])
    bill = Reception.departure(id)
    return str(bill)


@app.route('/get_status', methods=['GET'])
def get_status():
    id = int(flask.request.args['id'])
    current_status = Reception.get_status(id)
    return str(current_status)


@app.route('/get_position', methods=['GET'])
def get_position_in_queue():
    id = int(flask.request.args['id'])
    current_position = Reception.get_position_in_queue(id)
    return str(current_position)


@app.route('/get_bill', methods=['GET'])
def get_bill_for_pay():
    id = int(flask.request.args['id'])
    bill = Reception.get_bill(id)
    return str(bill)


def main():
    app.run('localhost', port=8000, debug=True)


if __name__ == '__main__':
    main()
