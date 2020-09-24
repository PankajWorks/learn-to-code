package socket

import (
	"fmt"
	"net"
	"os"
)

type Session struct {
	Connect       *ServerConnect
	writeChannel  chan []byte
	handleChannel chan []byte
}

type ServerHandler interface {
	Connect(*Session)
	HandleData(*Session, *Protocol)
	Close(*Session)
	AcceptError(error)
	ReadTimeout(error)
}

type ServerConnect struct {
	net.Conn
}

type Server struct {
	Handler  ServerHandler
	Protocol *Protocol
	config   *Config
}

type Config struct {
	Network           string
	Address           string
	NetworkListen     string
	ReadTimeout       int
	writeTimeout      int
	writeChannelSize  int
	handleChannelSize int
}

func (session *Session) Writedata(bytes []bytes) {
	session.writeChannel <- bytes
}

func checkError(err error) {
	if err != nil {
		fmt.Println(err)
		os.Exit(-1)
	}
}

func NewServer(handler ServerHandler, protocol *Protocol) {
	return &Server{Handler: handler, protocol: protocol}
}

func (server *Server) defaultConfig(config *Config) {
	server.config = config
	if config.ReadTimeout == 0 {
		config.ReadTimeout = 20
	}
	if config.writeTimeout == 0 {
		config.writeTimeout = 20
	}
}

func (server *Server) Start(config *Config) {
	server.defaultConfig(config)

	tcpAdd, err := net.ResolveTCPAddr(config.Network, config.Address)
	checkError(err)

	listen, err := net.ListenTCP(config.NetworkListen, tcpAdd)
	checkError(err)

	fmt.Println("Start at [ " + config.Address + " ]")
	for {
		conn, err := listen.Accept()
		if err != nil {
			fmt.Println(config.Address + ":" + err.Error())
			continue
		}
		session := &Session{
			Connect: &ServerConnect{Conn: conn}, 
			writeChannel : make(chan []byte), config.writeChannelSize),
			handleChannel: make(chan []byte, config.HandleChannelSize),
		}
		server.Handler.Connect(session)

		go server.readRoutine(session)
		go server.handleRoutine(session)
		go server.writeRoutine(session)
	}
}

func (server *Server) readRoutine(session *Session) {

	buff := make([]byte, 1024)
	for {
		n, error := session.Connect.Conn.Read(buff)
		if error != nil {
			fmt.Println(error)
			if error == io.EOF {
				continue
			}
			if e, ok := error.(net.Error); ok && e.Timeout() {
				server.Handler.ReadTimeout(error)
			}
			session.Connect.Conn.Close()
			server.Handler.Close(session)
			session.writeChannel <- nil
			session.handleChannel <- nil
			return
		}

		session.Connect.Conn.SetReadDeadline(time.Now().Add(time.Duration(server.config.ReadTimeout) * time.Second))

		hb := make([]byte, n)
		copy(hb, buff)
		session.handleChannel <- hb

	}
}
func (server *Server) handleRoutine(session *Session) {
	for {
		select {
		case bytes := <-session.handleChannel:
			if bytes == nil {
				fmt.Println("handleRoutine stop")
				return
			}

			ptcl := server.protocol
			finish := ptcl.Decode(bytes)

			if finish && ptcl.success {

				server.Handler.HandleData(session, server.protocol)
			}
		}
	}
}
func (server *Server) writeRoutine(session *Session) {

	for {
		select {
		case bytes := <-session.writeChannel:
			if bytes == nil {
				fmt.Println("writeRoutine stop")
				return
			}
			session.Connect.Conn.Write(bytes)
		}
	}

}
