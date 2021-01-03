##############################################
#
#   In effort to shorten the ridiculous import
#   lengths, this module imports a ton of
#   common modules from rantlib. This file is
#   just a curated list of imports. If you
#   need something that isn't here, use the
#   rantlib module
#
##############################################

# Interfacing with the devRant API
import rantlib.devrant.devrant as devRant
import rantlib.devrant.ezrant

# Generic application items
import rantlib.app.storage
import rantlib.app.client
import rantlib.app.event
import rantlib.app.lang
import rantlib.app.account