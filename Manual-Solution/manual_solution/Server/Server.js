var express = require('express');
var cors = require('cors');
var bodyParser = require('body-parser');
var latestRound = null;
var gameEndpoint = null;

apiServer = express();
apiServer.use(bodyParser.json({limit: '100mb', extended: true}))
apiServer.use(bodyParser.urlencoded({limit: '100mb', extended: true}))
apiServer.use(cors());
var exec = require('child_process').execFile;

apiServer.listen(50123, () => {
  console.log('API app listening on port 50123!');
})

apiServer.get('/startGame', function (req, res) {
    latestRound = null;
    /*exec('ic20_windows.exe',['-t','0'],
        function (error, stdout, stderr) {
            console.log('stdout: ' + stdout);
            console.log('stderr: ' + stderr);
            if (error !== null) {
                console.log('exec error: ' + error);
            }            
        }); */
        res.json({success: true});        
});

// Game sends round infos here
apiServer.post('/', function(req, res) {
  gameEndpoint = res;
  console.log(req.body.outcome);
  // zwischengespeicherte neuste Runde
  latestRound = req.body;
  console.log("Round received from game exe");
});

// API sends latest Round to Frontend
apiServer.get('/getRound', function (req, res) {
  console.log("getRound called from Frontend");
  //console.log("lastest round: " + latestRound)
  res.send(latestRound);
  console.log("latest Round was sent to Frontend");
});

// User Action from Frontend
apiServer.post('/sendAction', function(req, res) {
  console.log("action receiving ...");
  gameEndpoint.send(req.body);
  gameEndpoint = null;
  console.log("User Action was send to game exe");
  //res.write({success: true});
})




function saveGameRound(json) {
  var fs = require("fs");
  console.log(typeof(json));
  fs.file
  fs.writeFile("./SaveGames/420/Round" + json["round"] + ".json", JSON.stringify(json), 'UTF-8', (err) => {
    if (err) {
        console.error(err);
        return;
    };
    console.log("File has been created");
  });
}

