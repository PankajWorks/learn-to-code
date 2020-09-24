package main

import (
	"fmt"

	"github.com/pankajworks/go/socket"
)

type ServerHandlerImp struct {
}

func (s *ServerHandlerImp) Connect(session *socket.Session) {

	fmt.Println("Connect : ")

}
func (s *ServerHandlerImp) HandleData(session *socket.Session, protocol *socket.Protocol) {

	if protocol.IsHeartBeat() {
		fmt.Println("ReadData : IsHeartBeat")
		d := protocol.Encode(nil)
		session.WriteData(d)
	} else {
		fmt.Println("ReadData :" + protocol.String())
		d := protocol.Encode(protocol.GetData())
		session.WriteData(d)
	}

}
func (s *ServerHandlerImp) Close(session *socket.Session) {

	fmt.Println("Close : ")
}
func (s *ServerHandlerImp) AcceptError(err error) {

	fmt.Println("AcceptError : " + err.Error())
}

func (s *ServerHandlerImp) ReadTimeout(err error) {
	fmt.Println("ReadTimeout : " + err.Error())
}
func main() {
	server := socket.NewServer(&ServerHandlerImp{}, &socket.Protocol{})
	server.Start(&socket.Config{
		Network: "tcp", Address: ":7777", NetworkListen: "tcp", ReadTimeout: 20})

}
