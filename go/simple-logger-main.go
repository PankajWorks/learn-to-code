package main

import (
	"fmt"

	"github.com/pankajworks/Code/go/simplelogger"
)

func main() {
	log, err := simplelogger.Open("/tmp/logs", "zmcqdb.log")
	if err != nil {
		fmt.Println("Open log file failed!", err)
		return
	}
	log.SetConsole(true)
	log.SetLevel(simplelogger.DEBUG)
	defer log.Close()

	log.Info("This is info test.\n")
	log.Debugln("This is debugln test.")

	str := "This is a string."
	num := 4869

	log.Debug("string: %s\nnumber: %d\n", str, num)
	log.Debugln(str, num)
}
