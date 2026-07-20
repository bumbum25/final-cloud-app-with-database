const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const  cors = require('cors')
const app = express()
const port = 3030;

app.use(cors())
app.use(require('body-parser').urlencoded({ extended: false }));

let reviews_file = "reviews.json";
let dealerships_file = "dealerships.json";
if (!fs.existsSync(reviews_file)) {
  reviews_file = "data/reviews.json";
}
if (!fs.existsSync(dealerships_file)) {
  dealerships_file = "data/dealerships.json";
}

const reviews_data = JSON.parse(fs.readFileSync(reviews_file, 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync(dealerships_file, 'utf8'));

let reviews_list = reviews_data['reviews'] || [];
let dealerships_list = dealerships_data['dealerships'] || [];

let useInMemory = false;

mongoose.connect("mongodb://localhost:27017/", {'dbName':'dealershipsDB', serverSelectionTimeoutMS: 2000})
  .then(() => {
    console.log("Connected to local MongoDB");
    initMongooseData();
  })
  .catch(() => {
    mongoose.connect("mongodb://mongo_db:27017/", {'dbName':'dealershipsDB', serverSelectionTimeoutMS: 2000})
      .then(() => {
        console.log("Connected to Docker MongoDB");
        initMongooseData();
      })
      .catch(() => {
        console.log("Could not connect to MongoDB. Operating in In-Memory fallback mode.");
        useInMemory = true;
      });
  });

const Reviews = require('./review');
const Dealerships = require('./dealership');

function initMongooseData() {
  try {
    Reviews.deleteMany({}).then(()=>{
      Reviews.insertMany(reviews_list);
    });
    Dealerships.deleteMany({}).then(()=>{
      Dealerships.insertMany(dealerships_list);
    });
  } catch (error) {
    console.log("Error initializing Mongoose data:", error);
  }
}

// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API")
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  if (useInMemory) {
    return res.json(reviews_list);
  }
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  const dealerId = parseInt(req.params.id);
  if (useInMemory) {
    const filtered = reviews_list.filter(r => r.dealership === dealerId);
    return res.json(filtered);
  }
  try {
    const documents = await Reviews.find({dealership: dealerId});
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  if (useInMemory) {
    return res.json(dealerships_list);
  }
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  const state = req.params.state;
  if (useInMemory) {
    const filtered = dealerships_list.filter(d => 
      d.state.toLowerCase() === state.toLowerCase() || 
      (d.st && d.st.toLowerCase() === state.toLowerCase())
    );
    return res.json(filtered);
  }
  try {
    const documents = await Dealerships.find({
      $or: [
        { state: state },
        { st: state }
      ]
    });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  const dealerId = parseInt(req.params.id);
  if (useInMemory) {
    const dealer = dealerships_list.find(d => d.id === dealerId);
    return res.json(dealer ? [dealer] : []);
  }
  try {
    const documents = await Dealerships.find({id: dealerId});
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

//Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  const data = JSON.parse(req.body);
  
  if (useInMemory) {
    const sorted = [...reviews_list].sort((a, b) => b.id - a.id);
    let new_id = sorted.length > 0 ? sorted[0].id + 1 : 1;
    const newReview = {
      "id": new_id,
      "name": data['name'],
      "dealership": parseInt(data['dealership']),
      "review": data['review'],
      "purchase": data['purchase'],
      "purchase_date": data['purchase_date'],
      "car_make": data['car_make'],
      "car_model": data['car_model'],
      "car_year": parseInt(data['car_year'])
    };
    reviews_list.push(newReview);
    return res.json(newReview);
  }

  const documents = await Reviews.find().sort( { id: -1 } )
  let new_id = documents.length > 0 ? documents[0]['id']+1 : 1

  const review = new Reviews({
		"id": new_id,
		"name": data['name'],
		"dealership": data['dealership'],
		"review": data['review'],
		"purchase": data['purchase'],
		"purchase_date": data['purchase_date'],
		"car_make": data['car_make'],
		"car_model": data['car_model'],
		"car_year": data['car_year'],
	});

  try {
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
		console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
