var AWS = require("aws-sdk");
var get_items = require('./get_items.js')
let awsConfig = {
    "region": "us-east-1",
    "endpoint": "http://dynamodb.us-east-1.amazonaws.com",
    "accessKeyId": "", "secretAccessKey": ""
};
AWS.config.update(awsConfig);

let docClient = new AWS.DynamoDB.DocumentClient();

exports.addItem = async function (UUID, array_name, item) {
	  get_items.getItems(UUID, array_name).then(async function(response) {
		console.log("yooo number 2")
		var arr_to_update = response[array_name]
		console.log("array to update: " + arr_to_update)
		arr_to_update.push(item)
		console.log(response)

    async function additem_callback(UUID, array) {
    return new Promise((resolve, reject) => {
   
    var params = {
        TableName: "wise-up",
        Key: { "UUID": UUID },
        UpdateExpression: "set " + array_name + " = :to_insert",
        ExpressionAttributeValues: {
            ":to_insert": arr_to_update
        },
	 //   ConditionExpression: "attribute_not_exists(performances.#number)",
        ReturnValues: "UPDATED_NEW"

    };
    docClient.update(params, function (err, data) {

        if (err) {
            console.log("users::update::error - " + JSON.stringify(err, null, 2));
	    resolve({"status": 400})
        } else {
            console.log("users::update::success "+JSON.stringify(data) );
	    resolve({"status": 200})
        }
    });
    })
    }
    const second_response = await additem_callback(UUID, arr_to_update)
    console.log("second response: " + JSON.stringify(second_response))
    return second_response
    })
}

function resolve(path, obj) {
    return path.split('.').reduce(function(prev, curr) {
        return prev ? prev[curr] : null
    }, obj || self)
}
function setData(key,val,obj) {
  if (!obj) obj = data; //outside (non-recursive) call, use "data" as our base object
  var ka = key.split(/\./); //split the key by the dots
  if (ka.length < 2) { 
    obj[ka[0]] = val; //only one part (no dots) in key, just set value
  } else {
    if (!obj[ka[0]]) obj[ka[0]] = {}; //create our "new" base obj if it doesn't exist
    obj = obj[ka.shift()]; //remove the new "base" obj from string array, and hold actual object for recursive call
    setData(ka.join("."),val,obj); //join the remaining parts back up with dots, and recursively set data on our new "base" obj
  }    
}


exports.addKeyValue = async function (UUID, map_name, key_path, value) {
	get_items.getItems(UUID, map_name).then(async function(response) {
		console.log("after .then in addKeyValue")
		console.log(response)
		var map_to_update = response[map_name]
		setData(key_path, value, map_to_update)

		async function addkeyvalue_callback(UUID, map_name, map) {
			return new Promise((resolve, reject) => {

				var params = {
        				TableName: "wise-up",
        				Key: { "UUID": UUID },
        				UpdateExpression: "set " + map_name + " = :to_insert",
        				ExpressionAttributeValues: {
            				":to_insert": map
        				},
        				ReturnValues: "UPDATED_NEW"
    				};
    				docClient.update(params, function (err, data) {

        				if (err) {
            					console.log("users::update::error - " + JSON.stringify(err, null, 2));
            					resolve({"status": 400})
        				} else {
            					console.log("users::update::success "+JSON.stringify(data) );
            					resolve({"status": 200})
        				}
    				});
    			})
    		}
    		const second_response = await addkeyvalue_callback(UUID, map_name, map_to_update)
    		console.log(second_response)
		console.log("second response ^")
		return second_response

	})	
}
