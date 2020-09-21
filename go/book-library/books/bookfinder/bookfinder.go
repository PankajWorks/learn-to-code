//go:generate mockery -name=BookFetcher
package bookfinder

import (
	"context"

	"github.com/pankajworks/Code/go/book_library/books"
)

type (
	BookFetcher interface {
		FindBookByID(ctx context.Context, bookID int) (books.Book, error)
	}

	Finder struct {
		fetcher BookFetcher
	}
)

func New(fetcher BookFetcher) Finder {
	return Finder{
		fetcher: fetcher,
	}
}

func (f Finder) FindBook(ctx context.Context, bookID int) (books.Book, error) {
	return f.fetcher.FindBookByID(ctx, bookID)
}
