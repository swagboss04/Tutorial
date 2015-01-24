#~~~~~~~~~~~~~~~#
# Questionnaire #
#~~~~~~~~~~~~~~~#

import os
import sys

name = raw_input "Hey, what's your name?"
age = input "How old are you?"
if age == "14" or "15":
  res = raw_input "Is this your first year with FIRST?"
    if res == "Yes" or "yes":
      print "Welcome!"
      #if res == "no" or "No" 
      #don't use above if else works
      else:
        print "Welcome back!"

