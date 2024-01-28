from flask import Flask, redirect, url_for, jsonify, request, flash, render_template, json
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

application = Flask(__name__)
login_manager = LoginManager(application)
login_manager.login_view = 'login'
application.config['SECRET_KEY'] = '12640892135285634'

slot_names = []
purchase_costs = []
received_per_slot = []
spent = 0
recived = 0
created = 0
edited = 0
deposit_amount = 0
total_received = sum(received_per_slot)
current_theme = 'default'

class User(UserMixin):

    def __init__(self, user_id):
        self.id = user_id


# Rest of the code remains the same

users = {
    'TBAADMIN': generate_password_hash('TBAADMIN'),
    'Melvin465': generate_password_hash('Max7957Melvin'),
    'Testdex': generate_password_hash('dex2024test'),
}


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@application.route('/admin')
@login_required
def admin():
    global deposit_amount
    return render_template('admin.html',
                           slot_names=slot_names,
                           purchase_costs=purchase_costs,
                           received_per_slot=received_per_slot,
                           spent=spent,
                           total_received=total_received,
                           created=created,
                           edited=edited,
                           deposit_amount=deposit_amount)


@application.route('/add', methods=['POST'])
@login_required
def add():
    global received, spent, created
    new_name = request.form['name']
    new_cost = request.form['cost']

    try:
        float_cost = float(new_cost)
    except ValueError:
        # Обработка случая, когда new_cost не является допустимым числом с плавающей точкой
        return redirect('/admin')

    if new_name and float_cost:
        spent += float_cost
        slot_names.append(new_name)
        purchase_costs.append(float_cost)
        received_per_slot.append(
            0)  # Инициализация суммы полученного для нового слота
        created += 1

    return redirect('/admin')


@application.route('/del/<int:index>')
@login_required
def delete(index):
    global spent, received_per_slot, created
    if index < len(slot_names):
        spent -= float(purchase_costs[index])
        received_per_slot.pop(
            index)  # Удаляем соответствующую сумму полученного при удалении слота
        del slot_names[index]
        del purchase_costs[index]
        created -= 1
    return redirect('/admin')


@application.route('/edit_received/<int:index>', methods=['POST'])
@login_required
def edit_received(index):
    global received_per_slot, edited
    new_received = request.form['new_received']
    if index < len(slot_names) and new_received:
        received_per_slot[index] += float(new_received)
        edited += 1
    return redirect('/admin')


@application.route('/api/data', methods=['GET'])
def get_data():
    total_received = sum(received_per_slot)
    data = {
        'slot_names': slot_names,
        'purchase_costs': purchase_costs,
        'received_per_slot': received_per_slot,
        'spent': spent,
        'total_received': total_received,
        'created': created,
        'edited': edited,
        'deposit_amount': deposit_amount,
        'current_theme': current_theme
    }
    # Сохраняем данные в файл data.json
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)

    # Возвращаем данные в формате JSON
    return jsonify(data)

@application.route('/view')
def viewers():
    total_received = sum(received_per_slot)
    global current_theme
    return render_template('view.html',
                           slot_names=slot_names,
                           purchase_costs=purchase_costs,
                           received_per_slot=received_per_slot,
                           spent=spent,
                           total_received=total_received,
                           created=created,
                           edited=edited,
                           deposit_amount=deposit_amount,
                           theme=current_theme,
                           current_theme=current_theme)


@application.route('/admin/update_deposit', methods=['POST'])
@login_required
def update_deposit():
    global deposit_amount
    # Получаем сумму депозита из формы
    deposit_amount = float(request.form['deposit_amount'])
    # Редиректим обратно на страницу админа
    return redirect(url_for('admin'))


@application.route('/api/reset', methods=['POST'])
@login_required
def reset_data():
    global slot_names, purchase_costs, received_per_slot, spent, recived, created, edited, deposit_amount
    slot_names = []
    purchase_costs = []
    received_per_slot = []
    spent = 0
    recived = 0
    created = 0
    edited = 0
    deposit_amount = 0

    return redirect(url_for('admin'))


@application.route('/apply_theme', methods=['POST'])
@login_required
def apply_theme():
    global current_theme
    data = request.get_json()
    current_theme = data.get('theme', 'default')
    return jsonify({'message': 'Theme updated successfully'}), 200


@application.route('/')
@login_required
def index():
    return render_template('index.html')


@application.route('/themes')
@login_required
def themes():
    return render_template('themes.html')


if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0', port=8888)
