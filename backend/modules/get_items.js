var AWS = require("aws-sdk");


let awsConfig = {
    "region": "us-east-1",
    "endpoint": "http://dynamodb.us-east-1.amazonaws.com",
    "accessKeyId": "", "secretAccessKey": ""
};
AWS.config.update(awsConfig);

let docClient = new AWS.DynamoDB.DocumentClient();



//////////////////
//MAIN FUNCTIONS//
//////////////////


exports.getItems = async function (UUID, items) {
    async function getitems_callback(UUID, items) {
    return new Promise((resolve, reject) => {
    params = {
	TableName: "wise-up",
	Key: {
	    "UUID": UUID
	},
	ProjectionExpression: items
    }
	console.log("after promise")
    docClient.get(params, function (err, data) {
        if (err) {
	    console.log("error")
            console.log("users::fetchOneByKey::error - " + JSON.stringify(err, null, 2));
            resolve({"status": 400})
	}
        else {
	    var response = data["Item"]
	    response["status"] = 200
	    response = response
	    console.log("users::fetchOneByKey::success - " + response);
	    resolve(response)
	}
    })
    })
    }
    const response = await getitems_callback(UUID, items)
    return response
}
