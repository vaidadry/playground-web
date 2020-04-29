from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, SelectField, BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired, url, Email


class ContactForm(FlaskForm):
    email = StringField(label='Email',
                        render_kw={
                            "placeholder": "Email",
                            "class": "form-control"},
                        validators=[
                            Email(message="Not a valid email address"),
                            DataRequired()])
    subject = StringField(label='Subject',
                          render_kw={
                              "placeholder": "Subject",
                              "class": "form-control"},
                          validators=[
                              DataRequired()])
    message = TextAreaField(label='Message',
                            render_kw={
                                "placeholder": "Enter your message",
                                "class": "form-control",
                                "rows": 3},
                            validators=[
                                DataRequired()])


class AddRecipeForm(FlaskForm):
    title = StringField(label='Title',
                        render_kw={
                            "placeholder": "Add title",
                            "class": "form-control"},
                        validators=[
                            DataRequired()])
    url = StringField(label='URL',
                      render_kw={
                          "placeholder": "Add url",
                          "class": "form-control"},
                      validators=[
                          url(message="Not a valid URL address"),
                          DataRequired()])
    selectmeal = SelectField(label='Select meal',
                             render_kw={
                                 "placeholder": "--select--",
                                 "class": "form-control"},
                             validators=[
                                 DataRequired()],
                             choices=[
                                 ('breakfast', 'breakfast'),
                                 ('brunch', 'brunch'),
                                 ('lunch', 'lunch'),
                                 ('dinner', 'dinner')])
    # # ('', '--select--') -  no functionality yet in WTFORMS for placeholder
    comfortfood = BooleanField(label='definitely a comfort food',
                               render_kw={
                                   'value': '1'})
    fish = BooleanField(label='one for fish craving days',
                        render_kw={
                            'value': '1'})

    # custom-val checks the beginning of URL adds http:// if needed
    def validate(self):
        if not (self.url.data.startswith("http://") or self.url.data.startswith("https://")):
            self.url.data = "http://" + self.url.data
        if not FlaskForm.validate(self):
            return False
        return True


class SafePassForm(FlaskForm):
    password = PasswordField(label='Password',
                             render_kw={
                                 "placeholder": "Enter your password",
                                 "class": "form-control"},
                             validators=[
                                 DataRequired()])
    human = BooleanField(label="i'm a hooman or a very smart cat",
                         render_kw={
                            'value': 'human'},
                         validators=[
                             DataRequired()])

