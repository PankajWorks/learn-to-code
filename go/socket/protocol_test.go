package socket

import (
	"fmt"
	"testing"
)

func TestProtocol_Decode(t *testing.T) {

	p := &Protocol{}
	e := p.Encode([]byte("aaa"))
	d := p.Decode(e)
	if d && p.success {
		fmt.Println(p.String())
	}

}
