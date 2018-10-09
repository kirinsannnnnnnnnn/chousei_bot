# docker container list --all | awk '{print$1}' | 
# while read -r f; 
# do 
#   if [ "CONTAINER" != "$f" ]; then 
#     docker rm -f "$f"; 
#   fi
# done;

# docker container list --all;

# docker image list --all | awk '{print$3}' | 
# while read -r f; 
# do 
#   if [ "IMAGE ID" != "$f" ]; then 
#     docker rmi -f "$f"; 
#   fi 
# done;

# docker image list --all;

# docker build --no-cache /Users/kirin/notebook/gym_branch/onboard/gym-progress/ -t gym; 
docker build /Users/kirin/notebook/gym_branch/onboard/gym-progress/ -t gym; 
docker run -p 8080:8080 gym
