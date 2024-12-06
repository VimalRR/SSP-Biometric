from typing import Union
from zk import ZK, const

from fastapi import FastAPI

app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}



# @app.get("/zk")
# async def zk():
#     conn = None
#     zk = ZK('192.168.1.104', port=4370, timeout=30)
#     try:
#         print ('Connecting to device ...')
#         conn = zk.connect()
#         print ('Disabling device ...')
#         conn.disable_device()
#         print ('Firmware Version: : {}'.format(conn.get_firmware_version()))
#         # print '--- Get User ---'
#         users = conn.get_users()
#         formatted_users = []
#         for user in users:
#             privilege = 'User'
#             if user.privilege == const.USER_ADMIN:
#                 privilege = 'Admin'

#             user_info = {
#             "UID": user.uid,
#             "Name": user.name,
#             "Privilege": privilege,
#             "Password": user.password,
#             "Group ID": user.group_id,
#             "User ID": user.user_id,
#         }
#             formatted_users.append(user_info)

#         print(formatted_users)

#         attendance = conn.get_attendance()
#         print("attendance",attendance)

#         # print ("Voice Test ...")
#         # conn.test_voice()
#         print ('Enabling device ...')
#         conn.enable_device()

#         return {"message": "Success", "users": formatted_users}
#     except Exception as e:
#         print ("Process terminate : {}".format(e))
#         return {"message": "Process terminate : {}".format(e)}
#     finally:
#         if conn:
#             conn.disconnect()


@app.get("/get_device_info")
async def DeviceInfo(ip:str):
    conn = None
    zk = ZK('192.168.1.'+ip, port=4370, timeout=30)
    try:
        conn = zk.connect()
        device_info = {
            "current_time": conn.get_time(),
            "firmware_version": conn.get_firmware_version(),
            "device_name": conn.get_device_name(),
            "serial_number": conn.get_serialnumber(),
            "mac_address": conn.get_mac(),
            "face_algorithm_version": conn.get_face_version(),
            "finger_algorithm": conn.get_fp_version(),
            "platform_information": conn.get_platform(),
            "extend_fmt": conn.get_extend_fmt(),
            "user_extend_fmt": conn.get_user_extend_fmt(),
            "face_fun_on": conn.get_face_fun_on(),
            "compat_old_firmware": conn.get_compat_old_firmware(),
            "network_info": {
                "ip": conn.get_network_params().get('ip'),
                "netmask": conn.get_network_params().get('mask'),
                "gateway": conn.get_network_params().get('gateway')
            },
            "pin_width": conn.get_pin_width(),
            "free_data": conn.free_data(),
            "refresh_data": conn.refresh_data()
        }

        return {"message": "Success", "device_info": device_info}
    except Exception as e:
        print ("Process terminate : {}".format(e))
        return {"message": "Process terminate : {}".format(e)}
    finally:
        if conn:
            conn.disconnect()


@app.get("/get_memory_info")
async def MemoryInfo(ip:str):
    conn = None
    zk = ZK('192.168.1.'+ip, port=4370, timeout=30)
    try:
        conn = zk.connect()
        conn.read_sizes()
        response = {
            "message": "Success",
            "memory_info": {
                "users": {
                    "used": conn.users,
                    "max": conn.users_cap
                },
                "fingerprint": {
                    "used": conn.fingers,
                    "max": conn.fingers_cap
                },
                "dummy": conn.dummy,
                "cards": conn.cards,
                "rec_cap": conn.rec_cap,
                "fingers_av": conn.fingers_av,
                "users_av": conn.users_av,
                "rec_av": conn.rec_av
            }
        }
        return response
    except Exception as e:
        print ("Process terminate : {}".format(e))
        return {"message": "Process terminate : {}".format(e)}
    finally:
        if conn:
            conn.disconnect()

@app.get("/get_users")
async def Users(ip:str):
    conn = None
    zk = ZK('192.168.1.'+ip, port=4370, timeout=30)
    try:
        conn = zk.connect()
        print ('Disabling device ...')
        conn.disable_device()
        print ('--- Get User ---')
        users = conn.get_users()
        response = []
        for user in users:
            privilege = 'User'
            if user.privilege == const.USER_ADMIN:
                privilege = 'Admin'
            user_info = {
                "UID": user.uid,
                "Name": user.name,
                "Privilege": privilege,
                "Password": user.password,
                "Group ID": user.group_id,
                "User ID": user.user_id,
            }
            response.append(user_info)
        return {"message": "Success", "users": response}
    except Exception as e:
        print ("Process terminate : {}".format(e))
        return {"message": "Process terminate : {}".format(e)}
    finally:
        if conn:
            conn.disconnect()

@app.get("/get_attendance")
async def Attendance(ip:str):
    conn = None
    zk = ZK('192.168.1.'+ip, port=4370, timeout=30)
    try:
        print ('Connecting to device ...')
        conn = zk.connect()
        print ('Firmware Version: : {}'.format(conn.get_firmware_version()))
        # print '--- Get User ---'
       
        attendance = conn.get_attendance()
        print("attendance",attendance)

        return {"message": "Success", "attendance": attendance}
    except Exception as e:
        print ("Process terminate : {}".format(e))
        return {"message": "Process terminate : {}".format(e)}
    finally:
        if conn:
            conn.disconnect()



@app.get('/live_capture')
async def live_capture(ip:str):
    conn = None
    zk = ZK('192.168.1.'+ip, port=4370, timeout=30)
    try:
        conn = zk.connect()
        print("Start live capture ...")
        response = []
        for _ in range(1):  # Capture up to 5 attendance records
            attendance = conn.live_capture()
            if attendance is None:
                pass
            print(list(attendance))
        return {"message": "Success", "attendance": list(attendance)}
    except Exception as e:
        print("Process terminate : {}".format(e))
        return {"message": "Process terminate : {}".format(e)}
    finally:
        if conn:
            conn.disconnect()
