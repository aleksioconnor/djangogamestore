from common.util import user_is_developer
from django import template

# Template tag definition
# This template tag can be used in any template to check if
# currently logged in user is a developer. Example syntax:
# {% if user|user_is_developer %}

register = template.Library()
@register.filter(name='user_is_developer')
def user_is_developer_filter(user):
  return user_is_developer(user)

