import redis from 'redis';
import { promisify } from 'util';

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);

async function displaySchoolValue(school) {
  try {
    const value = await getAsync(school);
    console.log(`${school}: ${value}`);
  } catch (err) {
    console.error(`Error retrieving value for ${school}: ${err.message}`);
  } finally {
    client.quit();
  }
}

displaySchoolValue('MIT');
displaySchoolValue('Harvard');