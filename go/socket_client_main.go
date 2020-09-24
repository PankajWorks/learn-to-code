package main

import (
	"fmt"
	"net"
	"time"

	"github.com/pankajworks/Code/go/socket"
)

func main() {
	hawkServer, err := net.ResolveTCPAddr("tcp4", "127.0.0.1:7777")
	if err != nil {
		fmt.Println(err)
		return
	}

	connection, err := net.DialTCP("tcp4", nil, hawkServer)
	if err != nil {
		fmt.Println(err)
		return
	}
	time.Sleep(10 * time.Second)
	protocol := &socket.Protocol{
		Version: 1,
		Reserve: 0,
	}
	connection.Write(protocol.Encode([]byte("Hello World")))

	sig := make(chan bool)
	go heartBeat(connection)
	go receive(connection, protocol, sig)
	<-sig
	connection.Close()

}

func heartBeat(con *net.TCPConn) {
	protocol := &socket.Protocol{
		Version: 1,
		Reserve: socket.HEART_BEAT,
	}
	ticker := time.Tick(10 * time.Second)

	count := 0
	for {
		select {
		case <-ticker:
			con.Write(protocol.Encode(nil))
			count++
			if count == 3 {
				return
			}

		}
	}
}

func receive(con *net.TCPConn, protocol *socket.Protocol, sig chan bool) {

	buff := make([]byte, 1024)
	for {
		n, error := con.Read(buff)
		if error != nil {
			fmt.Println(error)
			break
		}
		finish := protocol.Decode(buff[0:n])
		if finish {
			if protocol.IsHeartBeat() {
				fmt.Println("receive from server: IsHeartBeat")
			} else {
				fmt.Println("receive from server: " + string(protocol.GetData()))
			}
		}

	}
	fmt.Printf("read finish")
	sig <- true
}
