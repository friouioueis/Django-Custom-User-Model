from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


ROLE_CHOICES = (
    ('si', 'simple'),
    ('rd', 'redacteur'),
    ('md', 'moderateur'),
    ('ad', 'admin')
)



class UtilisateurManager(BaseUserManager):
    def create(self, email, nomUtilisateur, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not nomUtilisateur:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            nomUtilisateur=nomUtilisateur,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nomUtilisateur, password):
        user = self.create(
            email=self.normalize_email(email),
            password=password,
            nomUtilisateur=nomUtilisateur,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class compteUtilisateur(AbstractBaseUser):
    idUtilisateur                   = models.AutoField(primary_key=True, editable=False)
    nomUtilisateur                  = models.CharField(max_length=30, unique=True, verbose_name="Nom d'utilisateur")
    email                           = models.EmailField(max_length=254, unique=True)
    date_joined				        = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				        = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				        = models.BooleanField(default=False)
    is_active				        = models.BooleanField(default=True)
    is_staff				        = models.BooleanField(default=False)
    is_superuser			        = models.BooleanField(default=False)


    USERNAME_FIELD = 'nomUtilisateur'
    REQUIRED_FIELDS = ['email']

    objects = UtilisateurManager()

    def __str__(self):
        return self.email + ': ' + self.nomUtilisateur

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class role(models.Model):
    idRole                          = models.AutoField(primary_key=True, editable=False)
    idUtilisateurR                  = models.ForeignKey(compteUtilisateur, on_delete=models.CASCADE, verbose_name='utilisateur')
    Type                            = models.CharField(max_length=2, choices=ROLE_CHOICES)

    def __str__(self):
        return self.get_Type_display() + ':' + self.idUtilisateurR.nomUtilisateur


class infoPersonel(models.Model):
    idInfoPer                       = models.AutoField(primary_key=True, editable=False)
    idUtilisateurIp                 = models.OneToOneField(compteUtilisateur, on_delete=models.CASCADE, verbose_name='utilisateur')
    nom                             = models.CharField(max_length=50)
    prenom                          = models.CharField(max_length=50)
    dateNaissance                   = models.DateField(verbose_name='Date de naissance')
    wilaya                          = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Infos Personnelles'
    def __str__(self):
        return 'Infos de: ' + self.idUtilisateurIp.nomUtilisateur
