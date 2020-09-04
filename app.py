from flask import Flask, render_template
app =  Flask(__name__)

posts = [
	{
		'author': 'Kamal Singh',
		'title': 'Blog Post 1',
		'content': 'First post Content',
		'date_posted': 'September 11, 2018'
	},
	{
		'author': 'Hikaru',
		'title': 'Blog Post 2',
		'content': 'Second post Content',
		'date_posted': 'January 08, 2019'
	}

]

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', posts = posts)

@app.route("/about")
def about():
	return render_template('about.html', title = 'About')

if __name__ == '__main__':
	app.run(debug=True)
