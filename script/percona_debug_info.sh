source ./percona_build_env.sh

CONF_FILE_PATH=${ROOT_PATH}/percona_server_impl.conf

echo "BUILD_DIR = $BUILD_DIR"
echo " --defaults-file=${CONF_FILE_PATH}"