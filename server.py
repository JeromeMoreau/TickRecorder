from flask import Flask,render_template,request,redirect, url_for
from app.tick_recorder import TickRecorder


app = Flask(__name__)

tickRecorder = TickRecorder()


@app.route('/')
def index():
    symbols = format_symbols(tickRecorder.symbol_list, tickRecorder.available_symbols())
    is_alive = tickRecorder.is_alive()
    keys = {'account_id': tickRecorder.account_id, 'token': tickRecorder.token}
    return render_template('index.html', symbols=symbols, is_alive=is_alive, keys=keys)


@app.route('/start')
def start_server():
    tickRecorder.start()
    return redirect(url_for('index'))


@app.route('/keys',methods=['POST'])
def change_keys():
    print('accountid: %s, token %s' %(request.form['account_id'],request.form['token']))
    tickRecorder.set_default_keys(accountId=request.form['account_id'],token=request.form['token'])
    return redirect(url_for('index'))


@app.route('/symbols',methods=['POST'])
def change_traded_symbols():

    traded_symbols = [symbol for symbol in tickRecorder.available_symbols() if request.form.get(symbol) is not None]

    print('traded symbols: ',traded_symbols)
    return redirect(url_for('index'))


def format_symbols(traded, available):
    symbols_dict = {}
    for symbol in available:
        if symbol in traded:
            symbols_dict[symbol]=True
        else:
            symbols_dict[symbol]=False
    return symbols_dict

if __name__ == '__main__':
    app.run(host='0.0.0.0')