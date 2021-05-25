/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
// Prepare arguments for cloudant action
function main_prep(params) {
    var selectors = {
        "_id": {
            "$gt": "0"
        }
    };
    if (params.state) {
        selectors.st = {
            "$eq": params.state
        };
    }
    return {
        "query": {
            "selector": selectors
        },
        "sort": [
            {
                "_id": "asc"
            }
        ]
    }
}

// Parse records action
function main_parse(params) {
    var res = {
        headers: {
            'Content-Type': 'application/json'
        },
        body: '<html></html>',
        statusCode: 200
    };
    if (!params || !params.docs) {
        res.stastusCode = 500;
    } else if (params.docs.length == 0) {
        res.stastusCode = 404;
    } else {
        res.body = {
            results: params.docs
        }
    }
    return res;
}

