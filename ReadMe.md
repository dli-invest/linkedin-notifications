# linkedin company scrap

Simple scrap to run linkedin using a github runner to allow for a consistent ip address.

For the first run on your runner, you need to use api_login to let linkedin authenticate you then you should be able to login normally.

the runner is self hosted on gcp

## References

screen -list 

screen -S runner -dm ./run.sh

screen -r runner

