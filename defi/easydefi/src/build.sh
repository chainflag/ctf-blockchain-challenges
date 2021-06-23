docker build -t "easydefi" .
docker run -d -p "0.0.0.0:8888:10001" -h "easydefi" --name="easydefi" -e TERM=xterm easydefi
