var AWS = require("aws-sdk");
var crypto = require('crypto')

//////////////////////
///HELPER FUNCTIONS///
//////////////////////
function uuidv4() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}
var rand = function() {
    return Math.random().toString(36).substr(2); // remove `0.`
};

var generate_token = function() {
    return rand() + rand(); // to make it longer
};

function hash_password(password) {
    var salt = crypto.randomBytes(128).toString('base64');
    var iterations = 10000;
    var hash_test = "";
    var hash = crypto.pbkdf2Sync(password, salt, iterations, 64, "sha1")
    return {
        "salt": salt,
        "hash": hash,
    };
}

function is_password_correct(hash, salt, iterations, password) {
	return hash.toString('hex') == crypto.pbkdf2Sync(password, salt, iterations, 64, "sha1").toString('hex');
}


let awsConfig = {
    "region": "us-east-1",
    "endpoint": "http://dynamodb.us-east-1.amazonaws.com",
    "accessKeyId": "", "secretAccessKey": ""
};
AWS.config.update(awsConfig);

let docClient = new AWS.DynamoDB.DocumentClient();



////////////////////
///MAIN FUNCTIONS///
////////////////////

//SIGN UP//
exports.signUp = async function (email, password) {

    var uuid = uuidv4()
    var hash_response = hash_password(password)
    var salt = hash_response["salt"]
    var hash = hash_response["hash"]

    var input = {
      	"UUID": uuid, "email": email, "hash": hash, "salt": salt, "dir": [], "files": [], "processing": 0};
    var params = {
        TableName: "wise-up",
        Item:  input
    };

    async function signup_callback(uuid, email) {
	return new Promise((resolve, reject) => {
    	    docClient.put(params, function (err, data) {
        	if (err) {
            	    console.log("users::save::error - " + JSON.stringify(err, null, 2));
	    	    resolve({"status": 400, "message": JSON.stringify(err, null, 2)})
        	} else {
            	    console.log("users::save::success");
	    	    resolve({"status": 200, "message": "successfull write", "user": {"UUID": uuid, "email": email, "dir": [], "files": []}})
        	}
	    });
	})
    }
    const response = await signup_callback(uuid, email)
    return response
}

//LOG IN//
exports.logIn = async function (email, password) {

    var params = {
	TableName: "wise-up",
	FilterExpression: 'email = :email_val',
	ExpressionAttributeValues: {
	    ":email_val": email
	}
    }
    async function login_callback(password) {
	return new Promise((resolve, reject) => {
	docClient.scan(params, function (err, data) {

        if (err) {
            console.log("users::fetchOneByKey::error - " + JSON.stringify(err, null, 2));
	    return_dictionary = {"status": 400}
            return {"status": 400, "message": JSON.stringify(err, null, 2)}
        } else {
	    console.log("email " + email + " and password " + password)
	    console.log("data not bgger than zero")
	    if (data.Items.length > 0) {
		var user_info = data.Items[0]
		var hash = user_info["hash"]
		var salt = user_info["salt"]
		var files = user_info["files"]
		var dir = user_info["dir"]
		console.log("password: ")
		console.log(password)
		console.log(salt)
		console.log("email " + email)
		if (is_password_correct(hash, salt, 10000, password)) {
			console.log("after password")
			console.log("users::fetchOneByKey::success - " + JSON.stringify(data, null, 2));
			const uuid = user_info["UUID"]
            		resolve({"status": 200, "message": "successfull read", "user": {'email': email, 'UUID': uuid, 'files': files, 'dir': dir}})
		}
		else {
			resolve({"status": 401, "message": "incorrect email or password"})
		}
	    }
	    else {
		return_dictionary = {"status": 401}
		return {"status": 401, "message": "incorrect email or password"}
	    }
        }
   
    });
    })
    }
    const response = await login_callback(password)
    return response
}
