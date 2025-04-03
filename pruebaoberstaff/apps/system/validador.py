import string
import secrets
from datetime import datetime, timezone
from apps.user.models import user, Token, keysRecovery
from .email1 import verificacionEmail, verificacionEmailUpdataUser


class validador():
    def __init__(self, user):
        self.user=user
    def GetCode(self):
        alphabet = string.ascii_letters + string.digits
        code = ''.join(secrets.choice(alphabet) for i in range(8))
        return code
    def ValidarEmail(self):
        
        num = 1
        while num >= 1:
            key = self.GetCode()
            num = keysRecovery.objects.filter(Status = True, keysRecovery=key).count()

        keys = keysRecovery.objects.create(
            user=self.user,
            keysRecovery = key
        )
        keys.save()
        verificacionEmail(codigo=key,to=self.user.email, name_user=self.user.Nombres)
        return True
    def ValidarCode(self, code):
        try:
            reg = keysRecovery.objects.filter(Status = True, keysRecovery=code)
            regis = reg.count()
            elemento = reg.first()
            if regis == 1:
                fecha_creacion = elemento.Creado
                fecha_ahora = datetime.now(timezone.utc)
                df = fecha_ahora - fecha_creacion
                if  df.seconds > 900:
                    elemento.Status=False
                    elemento.save()
                    return False
                else:
                    elemento.Status=False
                    elemento.save()
                    self.user.validacion_lvl2_email=True
                    self.user.save()
                    return True
            else:
                return False
        except Exception as e:
            print(e)
            return False