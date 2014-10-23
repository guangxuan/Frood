#Read https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#
#And http://vanderwijk.info/blog/adding-css-classes-formfields-in-django-templates/
'''
from django import template
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})
'''
from django import template
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
  attrs = {}
  definition = css.split(',')

  for d in definition:
    if ':' not in d:
      attrs['class'] = d
    else:
      t, v = d.split(':')
      attrs[t] = v

  return field.as_widget(attrs=attrs)