from app import app

PORT = 8080

if __name__ == "__main__":
    print "Server is listening to port {}".format(PORT)
    app.run(port=PORT)

