package booklistfinder_test

import (
	"context"
	"testing"

	"github.com/pankajworks/Code/go/book_library/books"
	"github.com/pankajworks/Code/go/book_library/books/booklistfinder"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

var expectedBooks = []books.Book{
	{
		ID:          1,
		Title:       "Livro de Teste",
		Description: "Esse livro é de teste",
		Author:      "Rafael Holanda",
		Edition:     1,
		BookShelf: books.Shelf{
			ID: 1,
		},
	},
	{
		ID:          2,
		Title:       "Livro de Teste 2",
		Description: "Esse livro é de teste 2",
		Author:      "Rafael Holanda",
		Edition:     1,
		BookShelf: books.Shelf{
			ID: 1,
		},
	},
}

func TestFinder_GetAllBooks(t *testing.T) {
	engine := new(mocks.BookListFindEngine)
	engine.On("FindAllBooks", mock.Anything).Return(expectedBooks, nil)
	finder := booklistfinder.New(engine)

	allBooks, err := finder.GetAllBooks(context.Background())

	assert.NoError(t, err)
	assert.Equal(t, expectedBooks, allBooks)
}
