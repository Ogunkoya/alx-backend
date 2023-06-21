const express = require('express');
const app = express();
const port = 1245;

// Route to get the list of available products
app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

// Start the server
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});