# knifeFight - Fight back against scammers

Scam text messages are fairly common these days, and the idea of them utterly disgusts me, they prey on people who are vulnerable.
Similar to the vein of my other work [^1] in calling out scammers / highlighting how bad they are, I give you a tool to fight back.
In fact, the reason why this tool is called `knifeFight` is due to my disdain for predatory organisations.

Scam text messages typically have a link in them, which is a phishing link. This link is used to steal your data, and is almost always a form which is sent to a server.
This tool is designed to spam the server with convincing-looking fake data, with typical drop-off points in the process to make it look like a real person.
Doing this will fill up their database with garbage and ruin their chances of seeing any signal amongst the noise.

This is quite a good strategy, as the phishing links are paid for by scammers, and sometimes they are paid per form submission.
This means that if you can fill up their database with garbage, you can make them lose a LOT of money.
On top of this, once they realise that their database is filling up with crap, they usually take down the link, which means that they can't scam anyone else.
This means even more money lost for them, as they had to put the work in to send out the scam text messages, and they got nothing in return, other than a fat bill for the form submissions.

`knifeFight.py` is a script which sends a boatload of fake data to scammers, filling up their database with garbage so it's a pain in the ass for them and may discourage them in the future (I hope).

So far you have to begin by manually doing the scam link, tracking the POST requests you send to them with browser dev tools (using the network tab - the pattern I noticed is it's always a few POST request).
Then copy the post request data and urls into `knifeFight.py` and use it to spam with fake data to your heart's content

## Usage

1. Create a bulk order on [Fake Name Generator](https://www.fakenamegenerator.com/order.php), be sure to grab as many fields as you can.
2. Alter `FAKE_NAME_GENERATOR_DATA` to point at your CSV data file.
3. Go to your target site and analyse what payloads (POST requests) for each step in the web form. Use the results to create fake payloads within `assemble_payloads`.
4. Let 'er rip.


## Kill Count

This script has been used on 7 scam text messages.
This was responsible for scammers trying to search for the source by doing a binary search one time, so it's obviously effective.

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
I turn the gun on them whenever our paths unfortunately cross. Call them out. Spend 15 minutes of your day making sure someone doesn't get ripped off, we all deserve someone to stand up for us.
I'm writing a blog post about this soon, with some of my investigative work.

