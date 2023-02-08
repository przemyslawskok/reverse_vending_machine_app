from functions.syntax import colors as c

def load_models(machine_class):
    try:

def compare_bottle_weight(bottle_info, communication_class):
    #check if diffrence is less than 10%
    if float(bottle_info[4]) * 0.9 < communication_class.WEIGHT_VALUE < float(bottle_info[4]) * 1.1:
        print(c.OK_GREEN+"Communication class: Measured weight: "+ str(communication_class.WEIGHT_VALUE) +"g. | DB weight: " + str(bottle_info[4]) + "g." + c.ENDC)
        return True
    else:
        print(c.ERROR+"Communication class: Measured weight: "+ str(communication_class.WEIGHT_VALUE) +"g. | DB weight: " + str(bottle_info[4]) + "g." + c.ENDC)
        return False

