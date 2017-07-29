# test container for WMH_challenge

INPUT_FOLDER='/mnt/DATA/datasets/test_challenge'
TEAM_NAME='nic-vicorob'
COMMAND='python test_net.py'

# build the contained
echo " "
echo "--------------------------------------------------"
echo "building container..."
echo "--------------------------------------------------"
echo " "
docker build -f Dockerfile -t wmhchallenge/$TEAM_NAME . 


# test the contained on different images
for im in `ls $INPUT_FOLDER`
do

    TEST_ORIG=$INPUT_FOLDER/$im/orig
    TEST_PRE=$INPUT_FOLDER/$im/pre
    RESULT_TEAM=$INPUT_FOLDER/$im

    
    echo " "
    echo "--------------------------------------------------"
    echo "testing on image " $RESULT_TEAM
    echo "folders:"
    echo " orig:"  $TEST_ORIG
    echo "  pre:"  $TEST_PRE
    echo "--------------------------------------------------"
    echo " "
    
    CONTAINERID=`nvidia-docker run -dit -v $TEST_ORIG:/input/orig:ro -v $TEST_PRE:/input/pre:ro -v /output wmhchallenge/$TEAM_NAME`
    time docker exec -it $CONTAINERID $COMMAND
    docker cp $CONTAINERID:/output $RESULT_TEAM
    docker stop $CONTAINERID
    docker rm -v $CONTAINERID
done
