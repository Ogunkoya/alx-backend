// Import necessary dependencies
import redis from 'redis';

// Create a Redis client
const client = redis.createClient();

// Handle the connection events
client.on('ready', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});