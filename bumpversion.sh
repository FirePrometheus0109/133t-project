#!/bin/bash

get_branch_name() {
    branch_name=$(git symbolic-ref -q HEAD)
    branch_name=${branch_name##refs/heads/}
    branch_name=${branch_name:-HEAD}
    echo ${branch_name}
}

CURRENT_BRANCH=$( get_branch_name )

if [ -f VERSION ]; then
    BASE_STRING=`cat VERSION`
    BASE_LIST=(`echo $BASE_STRING | tr '.' ' '`)
    V_MAJOR=${BASE_LIST[0]}
    V_MINOR=${BASE_LIST[1]}
    V_PATCH=${BASE_LIST[2]}
    echo "Current version : $BASE_STRING"
    V_MINOR=$((V_MINOR + 1))
    V_PATCH=0
    SUGGESTED_VERSION="$V_MAJOR.$V_MINOR.$V_PATCH"
    read -p "Enter a version number [$SUGGESTED_VERSION]: " INPUT_STRING
    if [ "$INPUT_STRING" = "" ]; then
        INPUT_STRING=$SUGGESTED_VERSION
    fi
    echo "Will set new version to be $INPUT_STRING"
    echo $INPUT_STRING > VERSION
    echo "Version $INPUT_STRING:" > tmpfile
    git log --pretty=format:" - %s" "$BASE_STRING"...HEAD >> tmpfile
    echo "" >> tmpfile
    echo "" >> tmpfile
    cat CHANGES >> tmpfile
    mv tmpfile CHANGES
    git add CHANGES VERSION
    git commit -m "[IMP]: bump version \`$BASE_STRING\` -> \`$INPUT_STRING\`"
    git tag -a $INPUT_STRING -m "Build $INPUT_STRING"
    git push origin $INPUT_STRING
    git push origin $CURRENT_BRANCH
else
    echo "Could not find a VERSION file"
fi
