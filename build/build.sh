# Variable Assignment
SCRIPT_BEING_RUN_ABSOLUTE_PATH=$0
NUMBER_OF_ARGUMENTS=$#

CURRENT_DIRECTORY=$(cd "$(dirname "$0")"; pwd)
REPOSITORY_ROOT_DIRECTORY="$(dirname "$CURRENT_DIRECTORY")"

BOT_NAME="grader_bot"

# Debugging
echo "SCRIPT_BEING_RUN_ABSOLUTE_PATH: $SCRIPT_BEING_RUN_ABSOLUTE_PATH"
echo "CURRENT_DIRECTORY: $CURRENT_DIRECTORY"
echo "REPOSITORY_ROOT_DIRECTORY: $REPOSITORY_ROOT_DIRECTORY"
echo "BOT_NAME: $BOT_NAME"

# Variable Assignment
echo "Executing: 'docker build $REPOSITORY_ROOT_DIRECTORY -f $REPOSITORY_ROOT_DIRECTORY/docker/Dockerfile -t $BOT_NAME'"
docker build $REPOSITORY_ROOT_DIRECTORY -f $REPOSITORY_ROOT_DIRECTORY/docker/Dockerfile -t $BOT_NAME