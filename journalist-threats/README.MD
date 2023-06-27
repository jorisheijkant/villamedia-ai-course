## Journalist threathened
This projects tries to find out more about journalists receiving threads on Twitter. It does so by using the Twitter API to collect tweets from journalists and then uses a machine learning algorithm to classify the tweets as threats or not threats.

### First dataset
In the first dataset we use the last 100 mentions of five well-known Dutch journalists. The journalists are (picked rather randomly from the Tegel nominations of 2021):

- [Jeroen Wollaars](https://twitter.com/jeroenwollaars)
- [Sinan Can](https://twitter.com/sinancan77)
- [Wafa Al Ali](https://twitter.com/alaliwafa)
- [Leen Vervaeke](https://twitter.com/leenvervaeke)
- [Yelle Tieleman](https://twitter.com/YelleTieleman)

The `tweets` folder contains a dataset (csv) for each journalist with 1000 replies to their account, including the date and sender info.