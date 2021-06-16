docker build -t "counter-strike" .
docker run -d -p "0.0.0.0:8888:10001" -h "counter-strike" --name="counter-strike" counter-strike