import socket
import classSea as cliCs

def click_join():
    # ip = socket.gethostbyname(socket.gethostname())
    # ip = "10.0.0.119"
    ip = input("Please input IP of the server: ")
    connect_port = 2019
    comms_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    comms_socket.connect((ip, connect_port))
    print("Connect to", ip)

    # arrange your ship
    enemySeaClient = cliCs.EnemySea()
    yourSeaClient = cliCs.YourSea()
    print("Let's play Battleship!")


    def client_send_dt(x):
        comms_socket.send(x.encode("UTF-8"))


    def layout():
        print("Enemy sea:")
        enemySeaClient.print_board(enemySeaClient.grid_en)
        print("Your sea:")
        yourSeaClient.print_board(yourSeaClient.grid_yo)
        # yourSeaClient.ships_info()


    layout()

    while True:
        # print("[Client] Connection Successful!!")
        # client input shoot point in server enemySea
        # send_data = input("Input your target [row][column]: ")
        passY, passX = enemySeaClient.target()
        send_data = str(passY) + str(passX)
        print(send_data)
        # client send point to server
        client_send_dt(send_data)
        # client get state flag from server to check if hit or not
        response = comms_socket.recv(64).decode("UTF-8")
        print(response)
        enemySeaClient.flag = int(response)
        print(enemySeaClient.flag)
        enemySeaClient.change_cell(passX, passY, enemySeaClient.flag) # changed
        # show game situation now
        layout()
        if enemySeaClient.flag == 2:
            print("You Win")
            comms_socket.close()
            break
        receive_pt = comms_socket.recv(64).decode("UTF-8")
        enemySeaClient.flag = str(yourSeaClient.check_shoot(int(receive_pt[1]), int(receive_pt[0]))) # changed
        yourSeaClient.draw_cell(int(receive_pt[1]), int(receive_pt[0]), str(enemySeaClient.flag))# changed
        layout()
        client_send_dt(enemySeaClient.flag)
        if enemySeaClient.flag == "2":
            print("You Loss")
            comms_socket.close()
            break
