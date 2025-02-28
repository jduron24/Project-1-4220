This is a flask project for our class



Below is a revised guide for setting up and accessing a local MongoDB instance on your computer so you can run our shared repository. This guide assumes that our repository already contains the necessary configuration (such as the connection string) and scripts for MongoDB access.

---

# Local MongoDB Setup & Access Guide

## 1. Install MongoDB

### macOS (Using Homebrew)
- **Install Homebrew** (if not already installed):
  ```sh
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
- **Install MongoDB Community Edition**:
  ```sh
  brew tap mongodb/brew
  brew install mongodb-community@6.0
  ```
- **Verify the installation**:
  ```sh
  mongod --version
  ```

### Windows & Linux
- Follow the [official MongoDB installation instructions](https://www.mongodb.com/docs/manual/installation/) for your operating system.

---

## 2. Start the MongoDB Server

1. **Create a data directory** (if needed):
   ```sh
   mkdir -p ~/data/db
   ```
2. **Launch MongoDB** by running:
   ```sh
   mongod --dbpath ~/data/db
   ```
   *Keep this terminal window open while you work.*

3. **Test the connection** by opening a new terminal and running:
   ```sh
   mongosh
   ```
   You should see the MongoDB shell prompt.

---

## 3. Configure the Project for Local MongoDB

- Our project is set up to use a local MongoDB instance by default. It connects using a URI like:
  ```
  mongodb://127.0.0.1:27017/MyLocalDB
  ```
- Make sure your environment variables (for example, in a `.env` file) point to this local URI. There is no need to change any code if you’re running locally.

---

## 4. Import Data (If Required)

If our repository includes exported JSON data for the database:

1. **Open a terminal** (while MongoDB is running) and navigate to the project directory.
2. **Import the data** using the following commands:
   - For the Users collection:
     ```sh
     mongoimport --db MyLocalDB --collection Users --file transformed_data1.json --jsonArray
     ```
   - For the PhotoGallery collection:
     ```sh
     mongoimport --db MyLocalDB --collection PhotoGallery --file transformed_data2.json --jsonArray
     ```
   *This will load the data into your local MongoDB instance.*

---

## 5. Verify the Setup

### Using the Mongo Shell
1. Open the Mongo shell:
   ```sh
   mongosh
   ```
2. Switch to the database:
   ```sh
   use MyLocalDB
   ```
3. Check the collections:
   ```sh
   db.Users.find().pretty()
   db.PhotoGallery.find().pretty()
   ```

### Using a Python Script
In our repository includes a verification script, run it to see a preview of the data:
```python

Run the script with:
```sh
python check_mongo.py
```

---

## 6. Summary

- **Install MongoDB** on your machine.
- **Start the MongoDB server** locally.
- **Ensure our project’s configuration** (via environment variables) uses the local URI (`mongodb://127.0.0.1:27017/MyLocalDB`).
- **Import any required data** using `mongoimport` (if not already present).
- **Verify the data** using either the Mongo shell or the provided Python script.

Following these steps will ensure you have a fully functional local MongoDB setup that mirrors our development environment. If you have any questions or encounter any issues, please reach out. Happy coding!
