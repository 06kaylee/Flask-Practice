from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) #start up a web server and if change in python code, automatically rerun web server