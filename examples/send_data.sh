#!/bin/bash
PORT=52001
echo "What do you want to send?"
read value
echo "Sending $value every second to port $PORT"
echo "Press CTRL-C to stop."
while echo $value;
 do 
    sleep 1
 done | nc -u localhost $PORT

