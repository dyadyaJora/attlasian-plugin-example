const express = require('express');
const bodyParser = require('body-parser');
const jwt = require('atlassian-jwt');
const request = require('request-promise');
const MongoClient = require('mongodb').MongoClient;

const app = express();

const url = process.env.MONGO_URI || 'mongodb://localhost:27017/';

let db, datas;

app.use(express.static('dist'));
app.use(bodyParser.json());

app.get('/', (req, res) => {
  res.end('This server serves up static files');
});

app.post('/app-installed-callback', (req, res) => {
  let baseUrl = req.body.baseUrl;
  let validation = true; // @todo

  if (!validation) {
    res.sendStatus(403);
    return;
  }

  datas.updateOne(
    { baseUrl: baseUrl },
    { $set: req.body },
    { upsert: true }
  );

  res.sendStatus(200);
});

app.get('/example', (req, res) => {
  let domain = 'https://qwertyqwery.atlassian.net';
  let task = 'TEST-2';

  datas.findOne({ baseUrl: domain })
    .then(data => {
      return getTask(domain, task, data.sharedSecret, data.key);
    })
    .then(data => {
       let resStr = task + '\n';
       resStr += getFullText(data);
       res.json({ data: resStr });
    })
    .catch(err => { res.sendStatus(400); console.log(err); });
});

app.use(function(req, res){
  res.sendStatus(404);
});

MongoClient.connect(url, (err, client) => {
  db = client.db(process.env.DB_NAME || 'jira-dev');
  datas = db.collection('datas');

  app.listen(8080);
})

function getTask(domain, task, secure, key) {
  let req = jwt.fromMethodAndUrl('GET', '/rest/api/3/issue/' + task);
  let qsh = jwt.createQueryStringHash(req);
  let data = {};
  data['iat']=new Date().getTime();
  data['exp']=data['iat']+1000*60*20;
  data['qsh']=qsh;
  data['iss']=key;
  let token = jwt.encode(data, secure);

  return request({
    uri: domain + '/rest/api/3/issue/' + task,
    qs: {
      jwt: token
    },
    json: true
  });
}

function getFullText(data) {
  let res = '';
  if (data.fields.description.content && data.fields.description.content) {
   data.fields.description.content.forEach(item => {
     if (item.type == 'paragraph' && item.content && item.content.length) {
       item.content.forEach( content => {
         if (content.text) {
           res += content.text + '\n';
         }
       });
     }
   });
  }
  return res;
}
