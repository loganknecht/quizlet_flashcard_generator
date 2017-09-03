# Variable Assignment
SCRIPT_BEING_RUN_ABSOLUTE_PATH=$0
NUMBER_OF_ARGUMENTS=$#

CURRENT_DIRECTORY=$(cd "$(dirname "$0")"; pwd)
REPOSITORY_ROOT_DIRECTORY="$(dirname "$CURRENT_DIRECTORY")"

DOCKER_IMAGE_TAG="quizlet_flashcard_maker"

# Debugging
echo "SCRIPT_BEING_RUN_ABSOLUTE_PATH: $SCRIPT_BEING_RUN_ABSOLUTE_PATH"
echo "CURRENT_DIRECTORY: $CURRENT_DIRECTORY"
echo "REPOSITORY_ROOT_DIRECTORY: $REPOSITORY_ROOT_DIRECTORY"
echo "DOCKER_IMAGE_TAG: $DOCKER_IMAGE_TAG"


rm -fr "$REPOSITORY_ROOT_DIRECTORY/output_directory/*"