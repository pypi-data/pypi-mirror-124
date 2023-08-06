import argparse

def main():
    parser = argparse.ArgumentParser(description="Upload a directory to the OSSR as record."
                                                 "The directory must include a valid zenodo or codemeta file to be used"
                                                 "as metadata source for the upload."
                                                 "If not record_id is passed, a new record is created."
                                                 "Otherwise, a new version of the existing record is created."
                                     )

    parser.add_argument('--token', '-t', type=str,
                        dest='zenodo_token',
                        help='Personal access token to (sandbox)Zenodo',
                        required=True)

    parser.add_argument('--sandbox', '-s', action='store',
                        type=lambda x: bool(strtobool(x)),
                        dest='sandbox_flag',
                        help='Set the Zenodo environment.'
                             'True to use the sandbox, False (default) to use Zenodo.',
                        default=False)

    parser.add_argument('--input-dir', '-i', type=str,
                        dest='input_directory',
                        help='Path to the directory containing the files to upload.'
                             'All files will be uploaded.',
                        required=True)

    parser.add_argument('--record_id', '-id', type=str,
                        dest='record_id',
                        help='record_id of the deposit that is going to be updated by a new version',
                        default=None,
                        required=False)

    parser.add_argument('--force-new-record',
                        action='store_true',
                        dest='force_new_record',
                        help='Force the upload of a new record in case a similar record is found '
                             'in the user existing ones',
                        )

    parser.add_argument('--no-publish',
                        action='store_false',
                        dest='publish',
                        help='Optional tag to specify if the record will NOT be published. '
                             'Useful for checking the record before publication of for CI purposes.',
                        )

    args = parser.parse_args()

    new_record_id = upload(args.zenodo_token,
                           args.sandbox_flag,
                           args.input_directory,
                           record_id=args.record_id,
                           force_new_record=args.force_new_record,
                           publish=args.publish)

    return new_record_id


if __name__ == '__main__':
    main()


REPOSITORY_NAME="$1"
REPOSITORY_ROOT_DIR="$2"
BUILD_DIR="$3"
REPOSITORY_URL=`git config --get remote.origin.url`
LAST_RELEASE=`git ls-remote --tags --refs --sort="v:refname" $REPOSITORY_URL | tail -n1 | sed 's/.*\///'`

mkdir -p $BUILD_DIR

if [ -z "$LAST_RELEASE" ]; then
    echo "No tag / new release found ! - Or error when parsing. Downloading last commit to the repository (master branch) ;"
    eossr-zip-repository -d $REPOSITORY_ROOT_DIR -n $REPOSITORY_NAME
    mv $REPOSITORY_NAME.zip $BUILD_DIR
else
    echo "$LAST_RELEASE tag / release found !"
    eossr-zip-repository -d $REPOSITORY_ROOT_DIR -n $REPOSITORY_NAME-$LAST_RELEASE
    mv $REPOSITORY_NAME-$LAST_RELEASE.zip $BUILD_DIR
fi

if [[ -f ./codemeta.json ]]; then
    cp ./codemeta.json ./zenodo_build
fi