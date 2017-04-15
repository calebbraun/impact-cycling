# -*- coding: utf-8 -*-
# impact-cycling (c) Caleb Braun

from flask_security import ConfirmRegisterForm
from flask_wtf.recaptcha import RecaptchaField


class ExtendedRegisterForm(ConfirmRegisterForm):
    recaptcha = RecaptchaField()

    def validate(self):
        rv = ConfirmRegisterForm.validate(self)
        if not rv:
            return False

        return True
