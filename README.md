# guess the outline

## introduction

This is a guess the outline game for the Q-E-D discord server. Try to guess the country in 3 or less guesses!

### running the app

#### python

first, copy all this code:
```bash
git clone https://github.com/samvandenabeele/guess-the-outline.git
```

Then, download the map from https://www.naturalearthdata.com/downloads/10m-cultural-vectors/ (admin 0) and put it under the `app/` folder.

After that, run
```bash
pip intall -r requirements.txt
```

now run 
```bash
python countries.py 
```

Now you are set to test the website!

to test the site, run

```bash
python run_prod.py
```

and navigate to `localhost:5000` in your browser of choice.

#### docker

first, pull the image from docker hub using:

```bash
docker pull samvandenabeele09/outlines:latest
```

then, run it using

```bash
docker run -d -p 5000:5000 --name outlines samvandenabeele09/outlines
```
