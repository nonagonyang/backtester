from flask import Flask, request, redirect, render_template,session,g,flash
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, Stock, StockPrice,Strategy,Backtest,User
from forms import BackTestingForm,UserAddForm,LoginForm
from apply_strategy import apply_strategy
from constants import *

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///python_trader_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"
    connect_db(app)
    return app

app=create_app()

CURR_USER_KEY = "curr_user"

##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/backtesting")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/stocks")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")



@app.route("/",methods=["GET", "POST"])
def homepage():
    if not g.user:
        form = LoginForm()

        if form.validate_on_submit():
            user = User.authenticate(form.username.data,
                                    form.password.data)

            if user:
                do_login(user)
                flash(f"Hello, {user.username}!", "success")
                return redirect("/stocks")

            flash("Invalid credentials.", 'danger')
        else:
            return render_template('index.html', form=form)
    else:
        user=User.query.filter_by(id=session[CURR_USER_KEY]).first()
        return render_template('user_details.html',user=user)



@app.route("/stocks")
def show_stocks():
    """
    Page with listing of stocks.
    Can take a 'q' param in querystring to search by that stock symbol.
    """
    search = request.args.get('q')
    if not search:
        stocks=Stock.query.order_by("symbol").all()
    else:
        stocks=Stock.query.filter(Stock.symbol.like(f"%{search}%")).all()

    return render_template("stocks.html",stocks=stocks)



@app.route("/stocks/<symbol>",methods=["GET", "POST"])
def stock_details(symbol):
    """
    Page with one specific stock, trading view picture and the most recent prices (opening, high, low, close) of this stock.
    """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    stock=Stock.query.filter_by(symbol=symbol).first()
    prices=StockPrice.query.filter_by(stock_id=stock.id).order_by(StockPrice.date.desc()).all()
    return render_template("prices.html",stock=stock,prices=prices)                                            


@app.route("/backtesting",methods=["GET", "POST"])
def new_test():
    """
    Page with a form that allows user to select parameters(stock, strategy, cash amount, start date, end date) as well as notes to perform backtest.
    """
    if not g.user:
        flash("Access unauthorized.Sign up or log in.", "danger")
        return redirect("/")
    form=BackTestingForm()
    form.strategy_id.choices = [(s.id, s.name) for s in Strategy.query.order_by('name')]
    form.stock_id.choices=[(stock.id, stock.symbol) for stock in Stock.query.order_by('symbol')]

    if form.validate_on_submit():
        user_id=session[CURR_USER_KEY]
        note=form.note.data
        cash_amount=int(form.cash_amount.data)
        strategy_id=int(form.strategy_id.data)
        strategy=Strategy.query.get(strategy_id)
        strategy_name=strategy.name
        stock_id=int(form.stock_id.data)
        stock=Stock.query.get(stock_id)
        stock_symbol=stock.symbol
        start_date=form.start_date.data
        end_date=form.end_date.data

        # apply_strategy returns a list of two values: result_cash and trading_logs
        result_cash=apply_strategy(cash_amount,stock_symbol,strategy_name,start_date, end_date)[0]
        if result_cash-cash_amount>0:
            result=f'You have earned {round((result_cash-cash_amount),2)}'
        else:
            result=f'You have lost {round((cash_amount-result_cash),2)}'
        trading_logs=apply_strategy(cash_amount,stock_symbol,strategy_name,start_date, end_date)[1]
        
        new_backtest=Backtest(stock_id=stock_id,strategy_id=strategy_id,user_id=user_id,
                start_date=start_date,end_date=end_date,
                initial_cash=cash_amount,result_cash=round(result_cash,2),result=result,trading_logs=trading_logs,note=note)
        db.session.add(new_backtest)
        db.session.commit()
        return redirect(f"/backtests/{new_backtest.id}")

    return render_template("backtesting.html",form=form)

@app.route("/backtests")
def show_backtests():
    """
    page show user's backtesting records
    """
    if not g.user:
        flash("Access unauthorized. Sign up or log in.", "danger")
        return redirect("/")
    user_id=session[CURR_USER_KEY]
    backtests=Backtest.query.filter_by(user_id=user_id).all()
    return render_template("backtest_results.html", backtests=backtests)

@app.route("/backtests/<backtest_id>")
def show_test_result(backtest_id):
    """
    page show one specific backtest's details: trading logs
    """
    if not g.user:
        flash("Access unauthorized. Sign up or log in.", "danger")
        return redirect("/")
    backtest=Backtest.query.filter_by(id=backtest_id).first()
    trading_logs=backtest.trading_logs.split('"')
    return render_template("backtest_details.html", backtest=backtest,trading_logs=trading_logs)

@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""
    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
