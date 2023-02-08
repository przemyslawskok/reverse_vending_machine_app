USB_VID_PID={
    "STM32":{               #NUCLEO-G070RB
        "VID":"1155",
        "PID":"14155",
    },
    "SCANNER":{     #2D Barcode Scanner Module MODEL: LV9500
        "VID":"59473",
        "PID":"8450",
    },
    "THERMAL_PRINTER":{     #RS232 Thermal Printer Module
        "VID":"1659",
        "PID":"8963",
    },
}


USB_BAUD_RATES={
    "STM32":{               #NUCLEO-G070RB
        "BAUD_RATE":"115200",
    },
    "SCANNER":{
        "BAUD_RATE":"9600",
    },
}

NUMBER_OF_SCANNERS = 6


#CAM UP CONFIG
CAM_UP_INDEX = 0
CAM_UP_Y_LOW= 0
CAM_UP_Y_HIGH = 480
CAM_UP_X_LOW = 80
CAM_UP_X_HIGH = 560



#CAM LID CONFIG
CAM_LID_INDEX = 1
CAM_LID_Y_LOW= 40
CAM_LID_Y_HIGH = 480
CAM_LID_X_LOW = 90
CAM_LID_X_HIGH = 530


ML_HOST = "127.0.0.1"
ML_PORT = 45455
ML_FACTOR = 45


FRONTEND_HOST = "127.0.0.1"
FRONTEND_PORT = 45456

BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 45457

PX_FACTOR = 8.5
