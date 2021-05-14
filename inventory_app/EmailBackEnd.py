from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    def authenticate(self,username=None, password=None, **kwargs):
        UserModel=get_user_model()
        try:
            user=UserModel.objects.get(phone=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None




# class EmailBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         UserModel = get_user_model()
#         if email is None:
#             phone = kwargs.get('phone')
#             if phone is None:
#                 return None
#             else:
#                 try:
#                     user = UserModel.objects.get(phone=phone)
#                 except UserModel.DoesNotExist:
#                     return None
#         else:
#             try:
#                 user = UserModel.objects.get(email=email)
#             except UserModel.Doesnotexist:
#                 return None
#
#         if user.check_password(password):
#             return user
#
#
#     def get_user(self, user_id):
#         UserModel = get_user_model()
#         try:
#             return UserModel.objects.get(id=user_id)
#         except UserModel.DoesNotExist:
#             return None
