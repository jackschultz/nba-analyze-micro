import numpy as np

from db.db import actor


values = {'fd': {}, 'dk': {}}

values['fd']['coef'] = 293.42862071
values['fd']['inter'] = -3927.43704516

def get_self_value(salary, proj_points, site='fd'):
   """Setting the value for a projection, where in this case, the value
       is the projected salary if the player had the projected points"""
   coef = values[site]['coef']
   inter = values[site]['inter']
   proj_salary = proj_points * coef + inter
   value =  proj_salary / salary
   return value

def get_self_value_pp36(salary, proj_pp36, site='fd'):
   """Setting the value for a projection, where in this case, the value
       is the projected salary if the player had the projected points"""
   coef = values[site]['coef']
   inter = values[site]['inter']
   proj_salary = proj_points * coef + inter
   value =  proj_salary / salary
   return value
