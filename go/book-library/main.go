package main

import (
	"net/http"

	"github.com/Fs02/rel"
	"github.com/Fs02/rel/adapter/mysql"
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
	"github.com/go-chi/render"
	_ "github.com/go-sql-driver/mysql"
	"github.com/pankajworks/Code/go/book_library/books/bookdeleter"
	"github.com/pankajworks/Code/go/book_library/books/bookfinder"
	"github.com/pankajworks/Code/go/book_library/books/booklistfinder"
	"github.com/pankajworks/Code/go/book_library/books/booksinserter"
	"github.com/pankajworks/Code/go/book_library/books/bookupdater"
	"github.com/pankajworks/Code/go/book_library/books/handler/bookdelete"
	"github.com/pankajworks/Code/go/book_library/books/handler/bookfind"
	"github.com/pankajworks/Code/go/book_library/books/handler/bookinsert"
	"github.com/pankajworks/Code/go/book_library/books/handler/booklistfind"
	"github.com/pankajworks/Code/go/book_library/books/handler/bookupdate"
	"github.com/pankajworks/Code/go/book_library/books/repository"
)

var dsn = "root:password@(localhost:3306)/library?parseTime=true"

func main() {
	router := chi.NewRouter()
	router.Use(middleware.Logger)
	router.Get("/ping", func(w http.ResponseWriter, r *http.Request) {
		render.PlainText(w, r, "pong")
	})

	adapter, err := mysql.Open(dsn)
	if err != nil {
		panic(err)
	}
	defer adapter.Close()

	// initialize rel's repo.
	repo := rel.New(adapter)
	repository := repository.New(repo)

	router.Method(http.MethodPost, "/books", bookinsert.NewHandler(booksinserter.New(repository, repository)))
	router.Method(http.MethodGet, "/books/{bookID}", bookfind.NewHandler(bookfinder.New(repository)))
	router.Method(http.MethodPut, "/books/{bookID}", bookupdate.NewHandler(bookupdater.New(repository)))
	router.Method(http.MethodDelete, "/books/{bookID}", bookdelete.NewHandler(bookdeleter.New(repository, repository)))
	router.Method(http.MethodGet, "/books", booklistfind.NewHandler(booklistfinder.New(repository)))

	err = http.ListenAndServe(":8080", router)
	if err != nil {
		panic(err)
	}
}
