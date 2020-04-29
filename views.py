import os

from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy

import checkmypass
import foodmood
import messenger

from forms import ContactForm, AddRecipeForm, SafePassForm

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'server.db')
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://tcmkffnivtqxpp:ba4ee87c931926ddae4332d3f3fcb9bc27d615fae310d8f67cb2162227d889ea@ec2-50-17-21-170.compute-1.amazonaws.com:5432/dfff403la84nvg'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '\xd7\xde"\t\x82\x10@\xd7\x15\xab)\xc3\rA\xc6\xe4\xbf~\xb1v\x01\x9e\xa7\xc1'
db = SQLAlchemy(app)

import models

@app.route('/')
@app.route('/home')
def my_home():
    return render_template('index.html')


# 404 erroras negali veikti del sito - kaip pataisyti?
@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


@app.route('/contact.html')
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    form = ContactForm()
    if form.validate_on_submit():
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        em = models.Email(email=email,
                          subject=subject,
                          message=message)
        db.session.add(em)
        db.session.commit()
        messenger.forward_message(form.data)
        return redirect('/thankyou.html')
    return render_template('/contact.html', form=form)


@app.route('/passwordchecker.html')
@app.route('/passchecked', methods=['POST', 'GET'])
def pass_check():
    form = SafePassForm()
    if form.validate_on_submit():
        data = request.form.to_dict()
        psw = data["password"]
        output = (checkmypass.main(psw))
        return render_template('/passchecked.html', output=output)
    return render_template('/passwordchecker.html', form=form)


@app.route('/foodmood', methods=['POST', 'GET'])
def choose_food():
    if request.method == 'POST':
        data = request.form.to_dict()
        # print(data)
        selectmeal = data['selectmeal']
        selections = data['selections']
        suggestion = foodmood.choose_dinner(selectmeal, selections)
        # print(suggestion)
        no_recipe = str('No recipes for this selection available. Contribute!')
        url = str(foodmood.select_url(suggestion))
        try:
            if suggestion != no_recipe:
                return render_template('/foodmood_suggestions.html', output=suggestion, output2=selectmeal, output3=url)
            else:
                return render_template('/foodmood_no_suggestion.html', output=suggestion, output2=selectmeal)
        except IndexError:
            # in case of specific selection is not on the Database
            return render_template('/foodmood_no_suggestion.html', output=suggestion, output2=selectmeal)
    else:
        return 'My apologies, Stranger! Something\'s wrong'


@app.route('/foodmood_add_suggestion.html')
@app.route('/add_suggestion', methods=['POST', 'GET'])
def add_suggestion():
    form = AddRecipeForm()
    if form.validate_on_submit():
        name = form.title.data.lower()
        comfortfood = form.comfortfood.data
        fish = form.fish.data
        meal = form.selectmeal.data
        recipe = foodmood.url_convert(form.url.data)
        if db.session.query(models.FoodMood).filter(models.FoodMood.name == name).count() == 0 \
                and db.session.query(models.FoodMood).filter(models.FoodMood.recipe == recipe).count() == 0:
            fm = models.FoodMood(name=name,
                                 comfortfood=comfortfood,
                                 fish=fish,
                                 meal=meal,
                                 recipe=recipe)
            db.session.add(fm)
            db.session.commit()
            return redirect('/thanks-contributor.html')
        return render_template('/foodmood_add_suggestion.html', form=form, message='Title or recipe URL already exists')
    return render_template('/foodmood_add_suggestion.html', form=form)


# not working temporarily
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500


if __name__ == "__main__":
    app.run()

