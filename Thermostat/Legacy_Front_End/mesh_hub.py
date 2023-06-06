import Communication
import time

comm = Communication.Communication("/dev/cu.AegisDongle", 115200)
def main():
    try:
        comm.setup()
        while(True):
            time.sleep(3)
            message = comm.receive_message()
            print(message)
    except Exception as e:
        print(e)
        comm.close()

"""
Main entrypoint for the application
"""
if __name__ == "__main__":
    main()
