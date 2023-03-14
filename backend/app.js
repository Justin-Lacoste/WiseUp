require("dotenv").config();
const http = require('http');
const fs = require('fs')
const url = require('url')
const jwt = require('jsonwebtoken')
var nStatic = require('node-static');
var fileServer = new nStatic.Server('./public');
const AWS = require('aws-sdk')
const s3 = new AWS.S3({
  accessKeyId: process.env.AWS_S3_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_S3_SECRET_ACCESS_KEY,
})

const hostname = '107.22.146.14'; // Your server ip address
const port = 3000;
var authentification = require('./modules/authentification.js')
var add_item = require('./modules/add_item.js')
var get_items = require('./modules/get_items.js')

function end_with_error_code(res, error_code) {
	res.statusCode = error_code
	res.end()
}

const server = http.createServer((req, res) => {

  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/html');
  
  if (req.url == '/') { //check the URL of the current request
  	fileServer.serve(req, res);      
        // set response content    
        //res.write('<html><body><p>This is Home Page.</p></body></html>');
//        res.writeHead(200, { 'content-type': 'text/html' })
//  	fs.createReadStream('index.html').pipe(res)
	//fs.createReadStream('index.css').pipe(res)
	//fs.createReadStream('index.html').pipe(res)
	  //res.end();

  }
  else if (req.url == "/signup") {

	const authHeader = req.headers['authorization']
        const email_password = authHeader && authHeader.split(' ')[1]
        if (email_password == null || !email_password.includes(":")) return end_with_error_code(res, 401)
        const email = email_password && email_password.split(':')[0]
        const password = email_password && email_password.split(':')[1]	

	authentification.signUp(email, password).then(function(response){
	    if (response["status"] == 400) return end_with_error_code(res, 400)
            if (response["status"] == 401) return end_with_error_code(res, 401)
            res.statusCode = 200
	    var UUID_object = { UUID: response['user']['UUID'] }
            const access_token = jwt.sign(UUID_object, process.env.ACCESS_TOKEN_SECRET)
            response["user"]["JWT"] = access_token  
	    console.log(response)
	    res.write(JSON.stringify(response))
	    res.end()
        });

  }
  else if (url.parse(req.url).pathname == "/get_info") {
	var UUID = url.parse(req.url,true).query.UUID
	
	get_items.getItems(UUID, "files").then(function(response) {
            	if (response["status"] == 400) {
		    res.statusCode = 400
		    res.write(JSON.stringify(response))
		    res.end()
		}
            	res.statusCode = 200
		console.log(response)
		res.statusCode = response["status"]
            	res.write(JSON.stringify(response))
            	res.end()
        })
  }
  else if (req.url == "/login") {

	const authHeader = req.headers['authorization']
        const email_password = authHeader && authHeader.split(' ')[1]
        if (email_password == null || !email_password.includes(":")) return end_with_error_code(res, 401)
	const email = email_password && email_password.split(':')[0]
	const password = email_password && email_password.split(':')[1]
	console.log("yo!")
	authentification.logIn(email, password).then(function(response) {

	    if (response["status"] == 400) return end_with_error_code(res, 400)
	    if (response["status"] == 401) return end_with_error_code(res, 401)
	    res.statusCode = 200
	    console.log("joe")
	    var UUID_object = { UUID: response['user']['UUID'] }
	    const access_token = jwt.sign(UUID_object, process.env.ACCESS_TOKEN_SECRET)
	    response["user"]["JWT"] = access_token
   	    console.log(JSON.stringify(response))
	    res.write(JSON.stringify(response))
            res.end()
	})
  }
  else if (url.parse(req.url).pathname == "/new_dir") {
	  var dir = url.parse(req.url,true).query.dir
	  var UUID = url.parse(req.url,true).query.UUID
	  console.log(dir)
	   add_item.addItem(UUID, "dir", dir).then(function(response){
                //res.write({"status": 200})
                res.end()
           });
  }
  else if (req.url == "/json_to_s3") {

	var jsonString = '';
        req.on('data', function (data) {
            jsonString += data;
        });
        req.on('end', async function () {
            jsonString = JSON.parse(jsonString);
	    console.log(req.body)
	    var filename = Math.floor(Math.random() * 100000000) + "-" + jsonString.title + ".json"//jsonString.filename.substring(0, jsonString.filename.length - 4) + ".json"
	    var UUID = jsonString.UUID
	    var directory = jsonString.directory
	    var data = JSON.stringify(jsonString.data)
	    console.log("filename " + filename + " with UUID " + UUID + " and data " + data) 
	    const uploadedImage = await s3.upload({
  		Bucket: process.env.AWS_S3_BUCKET_NAME,
  		Key: filename,
  		Body: data
	    }).promise()

	    add_item.addItem(UUID, "files", {"title": jsonString.filename, "s3": filename, "dir": directory}).then(function(response){
	    	//res.write({"status": 200})
	    	res.end()
            });
	});

	res.end()
  }
  else if (req.url == "/admin") {

        // set response content
        res.write('<html><body><p color="red">This is Admin Page.</p></body></html>');
        res.end();

  }else{
        // set Invalid response content
        //res.statusCode = 401;
	
//	var filename = url.parse(req.url).pathname.substring(1);
	//fs.readFile('./' + filename, function(err, data) {
        //    res.end(data);
        //});
//	if (fs.existsSync(filename)) {
//		res.writeHead(200, { 'content-type': 'text/html' })
//        	fs.createReadStream(filename).pipe(res)
//	}
	fileServer.serve(req, res);
	//console.log(url.parse(req.url).pathname)
        //res.end();
  }

  console.log(`New request => http://${hostname}:${port}`+req.url);
});

server.listen(port, '0.0.0.0', () =>{
  console.log(`Server running at http://${hostname}:${port}/`);
});
