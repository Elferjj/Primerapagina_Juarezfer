from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.db.utils import IntegrityError, OperationalError 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, 'profile') or Profile.objects.filter(user=instance).count() == 0:
            try:
                Profile.objects.create(user=instance)
            except (IntegrityError, OperationalError) as e:
                print(f"DEBUG: Error al crear perfil para {instance.username}: {e}. "
                      "Esto indica que el perfil ya podría existir, lo cual es inusual para un usuario nuevo.")
                
                pass
        else:
            print(f"DEBUG: create_user_profile: Perfil para {instance.username} ya existe, no se crea uno nuevo.")



@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        
        if not hasattr(instance, 'profile') or Profile.objects.filter(user=instance).count() == 0:
            try:
                Profile.objects.create(user=instance)
                print(f"DEBUG: save_user_profile: Perfil creado lazily para {instance.username} porque no existía.")
            except (IntegrityError, OperationalError) as e:
                print(f"DEBUG: save_user_profile: Error al crear perfil lazily para {instance.username}: {e}")
        else:
            print(f"DEBUG: save_user_profile: Profile.DoesNotExist para {instance.username} "
                  "pero instance.profile existe, no se hace nada.")
    except (IntegrityError, OperationalError) as e:
        print(f"DEBUG: save_user_profile: Error inesperado al guardar perfil para {instance.username}: {e}")
        pass 