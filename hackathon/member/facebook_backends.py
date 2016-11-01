from django.contrib.auth import get_user_model
User = get_user_model()


class FacebookBackend:
   def authenticate(self, user_info, token=None):
       try:
           user = User.objects.get(facebook_id=user_info["id"])
           return user
       except:
           user = User.objects.create_user(user_info)
           return user

   def get_user(self, user_id):
       try:
           return User.objects.get(pk=user_id)
       except:
           return None