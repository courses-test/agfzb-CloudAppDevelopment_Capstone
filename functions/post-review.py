#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys

# Prepare clodant results action
def main(dict):
    if dict and dict.docs:
        return { "results": dict.docs }
    else:
        return { "results": []}
