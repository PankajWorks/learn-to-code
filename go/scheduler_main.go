package main

import (
	"fmt"

	"github.com/pankajworks/Code/go/scheduler"
)

func main() {
	s, err := scheduler.NewScheduler(1000)
	if err != nil {
		panic(err) // just example
	}

	// delay with 1 second, job function with arguments
	s.Delay().Second(1).Do(task1, "prprprus", 23)

	// delay with 1 minute, job function without arguments
	s.Delay().Minute(1).Do(task2)

	// delay with 1 hour
	s.Delay().Hour(1).Do(task2)

	// special: execute immediately
	s.Delay().Do(task2)

	// cancel job
	jobID := s.Delay().Day(1).Do(task2)
	err = s.CancelJob(jobID)
	if err != nil {
		panic(err)
	} else {
		fmt.Println("cancel delay job success")
	}

	s1, err := scheduler.NewScheduler(1000)
	if err != nil {
		panic(err)
	}

	// Specifies time to execute periodically
	s1.Every().Second(45).Minute(20).Hour(13).Day(23).Weekday(3).Month(6).Do(task1, "prprprus", 23)
	s1.Every().Second(15).Minute(40).Hour(16).Weekday(4).Do(task2)
	s1.Every().Second(1).Do(task1, "prprprus", 23)

	// special: executed once per second
	s1.Every().Do(task2)

	// cancel job
	jobID := s.Every().Second(1).Minute(1).Hour(1).Do(task2)
	err = s1.CancelJob(jobID)
	if err != nil {
		panic(err)
	} else {
		fmt.Println("cancel periodically job success")
	}
}
