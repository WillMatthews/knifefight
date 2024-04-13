
# knifeFight - Fight back against scammers

Scam text messages are fairly common these days, and the idea of them utterly disgusts me, they prey on people who are vulnerable.
Similar to the vein of my other work [^1] in calling out scammers / highlighting how bad they are, I give you a tool to fight back.
In fact, the reason why this tool is called `knifeFight` is due to my disdain for predatory organisations.

`knifeFight.py` is a script which sends a boatload of fake data to scammers, filling up their database with garbage so it's a pain in the ass for them and may discourage them in the future (I hope).

So far you have to begin by manually doing the scam link, trackng the POST requests you send to them with browser dev tools (using the network tab - the pattern I noticed is it's always a few POST request).
Then copy the post request data and urls into `knifeFight.py` and use it to spam with fake data to your heart's content


## Future Vision

My future vision for this tool is that you should be able to paste a link in, it will figure everything out, and then will blast them into the ground.
No need for faffing about with tracking POST requests.


## Caveats

Currently this is kind of garbage and requires some hacking to get it working for each case. I know how bad this is, and will fix it up soon.


## Todos
- [ ] Multiprocessing for more spamming
- [ ] Better Docs
- [ ] Better Setup (currently it's garbage)
- [ ] Use fakedata better (create a big dict, and then just call from dict rather than row indexes)
- [ ] Better randomness for failing points in the process
- [ ] Better randomness for data (more entropy in fake names etc)
- [ ] Use a LLM to randomly generate some garbage data too? More entropy this way?


# Tips

Don't blast every single text - one time they tried to binary search for me after I did six in a row, and I just stopped. They sent approx 12 scam texts in an hour timespan.

[^1]: 'Stop Knife Crime' is a 'cause' which is run by Inside Success UK, a sinister, predatory organisation which is known for [harassing and intimidating the public to force them into making donations.](https://docere.uk/articles/the-london-knife-crime-activists)
I turn the gun on them whenever our paths unfortuantely cross. Call them out. Spend 15 minutes of your day making sure someone doesn't get ripped off, we all deserve someone to stand up for us.
I'm writing a blog post about this soon, with some of my investigative work.
