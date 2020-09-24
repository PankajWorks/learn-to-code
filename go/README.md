

## Migration
- Migration library used - https://github.com/rubenv/sql-migrate
- https://povilasv.me/go-schema-migration-tools/

```bash
# Running migration for book_library
cd book_library
sql-migrate up -env="test"
```

## Mockery
- https://github.com/jaytaylor/mockery-example
```bash
mockery --all
```

## Build HTTP
- [lightweight, idiomatic and composable router for building Go HTTP services.](https://github.com/go-chi/chi)


## Database
- [Golang SQL Database Layer for Layered Architecture.](https://fs02.github.io/rel/#/)

## Packaging
- https://golang.org/ref/mod#go-mod-vendor

## Log
- [The zerolog package provides a fast and simple logger dedicated to JSON output](https://github.com/rs/zerolog)

)
## References
- [Fix 'this authentication plugin is not supported' issue while using Go to connect MySQL 8](https://www.pixelstech.net/article/1531316568-Fix-this-authentication-plugin-is-not-supported-issue-while-using-Go-to-connect-MySQL-8)
- [Go Packages](https://golang.org/pkg/)

## Starting a new project

```bash
go mod init github.com/pankajworks/Code/go
go build
go mod vendor
```