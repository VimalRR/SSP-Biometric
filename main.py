from typing import Union
from zk import ZK, const

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/zk")
async def zk():
    conn = None
    zk = ZK('192.168.1.151', port=4370, timeout=30)
    try:
        print ('Connecting to device ...')
        conn = zk.connect()
        print ('Disabling device ...')
        conn.disable_device()
        print ('Firmware Version: : {}'.format(conn.get_firmware_version()))
        # print '--- Get User ---'
        users = conn.get_users()
        for user in users:
            privilege = 'User'
            if user.privilege == const.USER_ADMIN:
                privilege = 'Admin'

            print ('- UID #{}'.format(user.uid))
            print ('  Name       : {}'.format(user.name))
            print ('  Privilege  : {}'.format(privilege))
            print ('  Password   : {}'.format(user.password))
            print ('  Group ID   : {}'.format(user.group_id))
            print ('  User  ID   : {}'.format(user.user_id))

        attendance = conn.get_attendance()
        print("attendance",attendance)

        # print ("Voice Test ...")
        # conn.test_voice()
        print ('Enabling device ...')
        conn.enable_device()
    except Exception as e:
        print ("Process terminate : {}".format(e))
    finally:
        if conn:
            conn.disconnect()