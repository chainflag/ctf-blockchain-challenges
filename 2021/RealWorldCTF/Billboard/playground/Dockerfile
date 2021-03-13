# > docker build -t playground .
FROM golang:alpine AS build-env

WORKDIR /go/src/github.com/iczc/billboard/playground

COPY . .

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o billboard-playground .

FROM alpine

RUN apk add --update ca-certificates
WORKDIR /app

COPY --from=build-env /go/src/github.com/iczc/billboard/playground/billboard-playground .

EXPOSE 8080

ENTRYPOINT ["./billboard-playground"]