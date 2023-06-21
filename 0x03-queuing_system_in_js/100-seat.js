const express = require('express');
const { promisify } = require('util');
const redis = require('redis');
const kue = require('kue');

const app = express();
const port = 1245;

// Create the Redis client
const redisClient = redis.createClient();

// Promisify Redis functions
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

// Initialize the number of available seats
const initialNumberOfSeats = 50;
setAsync('available_seats', initialNumberOfSeats);

// Initialize reservationEnabled
let reservationEnabled = true;

// Function to reserve a seat
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

// Function to get the current number of available seats
async function getCurrentAvailableSeats() {
  const numberOfAvailableSeats = await getAsync('available_seats');
  return Number(numberOfAvailableSeats);
}

// Create a Kue queue
const queue = kue.createQueue();

// Process the queue
queue.process('reserve_seat', async (job, done) => {
  const currentAvailableSeats = await getCurrentAvailableSeats();
  const requestedSeats = job.data.seats;

  if (currentAvailableSeats >= requestedSeats) {
    const newAvailableSeats = currentAvailableSeats - requestedSeats;
    await reserveSeat(newAvailableSeats);

    if (newAvailableSeats === 0) {
      reservationEnabled = false;
    }

    done();
  } else {
    done(new Error('Not enough seats available'));
  }
});

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

// Route to process the queue
app.get('/process', (req, res) => {
  if (reservationEnabled) {
    queue.create('reserve_seat', { seats: 1 }).save();

    res.json({ status: 'Queue processing' });
  } else {
    res.status(403).json({ error: 'Reservation not available' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});