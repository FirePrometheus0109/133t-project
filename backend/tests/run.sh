#!/bin/sh

# The file is not intended to run by hand, instead use
# docker-compose -f docker-compose.autotest.yml run backend_autotest tests/run.sh
# or execute run_all_tests.sh from the root of the project

printf "\n>>>>>>>>> prospector <<<<<<<<<\n\n"
/maintainer-quality-tools/prospector_quality_check
RESULT="$?"

# check result of rsync db's
if [ "$RESULT" != "0" ]; then
    echo -e "prospector_quality_check exit Code:" $RESULT "\nFAILED"
    exit ${RESULT}
else
    echo "prospector_quality_check SUCCESSFULL"
fi

printf "\n>>>>>>>>> Django tests <<<<<<<<<\n\n"
pytest /app/tests/
coverage-badge > htmlcov/coverage.svg
