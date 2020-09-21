//go:generate mockery -name=UpdaterEngine
package bookupdater

import (
	"context"

	"github.com/pankajworks/Code/go/book_library/books"
)

type (
	UpdaterEngine interface {
		UpdateBook(ctx context.Context, book books.Book) error
	}

	Updater struct {
		engine UpdaterEngine
	}
)

func New(engine UpdaterEngine) Updater {
	return Updater{
		engine: engine,
	}
}

func (u Updater) UpdateBook(ctx context.Context, book books.Book) error {
	return u.engine.UpdateBook(ctx, book)
}
