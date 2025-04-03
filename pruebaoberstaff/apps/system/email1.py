from django.template.loader import render_to_string
import os
from envialosimple.transaccional import Transaccional
from envialosimple.transaccional.mail import MailParams

def verificacionEmail(codigo=1122, to="", name_user=""):

    try:
        estr = Transaccional(os.environ.get("API_MAIL"))
        html_content = render_to_string(
            "email/validaremail.html",
            context={"codigo": codigo},
        )
        params = MailParams(
                from_email='jhocce.briceno@clubziko.com', 
                from_name='Jhocce de clubziko.com',
                to_email=to, 
                to_name=name_user,
                # reply_to='reply@here.com',
                subject='Hola {0}, por favor verifica tu correo..'.format(name_user), 
                preview_text='Verificación de correo en clubziko.com...',
                html=html_content, 
                text=html_content,
                context={'name': name_user})

        estr.mail.send(params)
       
    except Exception as e:
        raise e


def verificacionEmailUpdataUser(codigo=1122, to="", name_user=""):

    try:
        estr = Transaccional(os.environ.get("API_MAIL"))
        html_content = render_to_string(
            "email/validaremailupdateuser.html",
            context={"codigo": codigo},
        )
        params = MailParams(
                from_email='jhocce.briceno@clubziko.com', 
                from_name='Jhocce de clubziko.com',
                to_email=to, 
                to_name=name_user,
                # reply_to='reply@here.com',
                subject='Hola {0}, por favor verifica esta acción..'.format(name_user), 
                preview_text='Verificación de correo en clubziko.com...',
                html=html_content, 
                text=html_content,
                context={'name': name_user})

        estr.mail.send(params)
       
    except Exception as e:
        raise e