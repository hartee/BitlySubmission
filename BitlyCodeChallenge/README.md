
# Bitly Coding Challenge
## _ErikAnthony Harte - erikanthony.harte@gmail.com_

---

## Dependencies:
Python version: python 3x

The (unzipped) data file is located at ./bitly/data/challenge.json

## To Install:
The code is located on GitHub: https://github.com/hartee/bitly-coding-challenge.git

---

## Design
The primary thought behind my solution is that the logic to determine if a sign-up event
is programmatic is likely to:
1. change frequently as we gain additional information, and
2. likely to be different depending on what attributes are considered.

Given this, I've designed the solution to include multiple validation classes, each
with different logic, looking at different attributes.  The idea is that as we
learn more about the logic that works, we can easily modify it.

Each event is presented to a set of validators, each of which assesses a score to the
event if certain logic is triggered.  A logger collects these scores and related
information.  If the accumulated scores pass a predetermined threshold an anomaly
is reported and the scores displayed.  The actual scores need to be tuned over time
by running it and comparing to actual results.

Because this is a demonstration rather than a production system, I've simplified things
a bit: I have a separate ingester class to read the JSON events from a file.  But
in a production system the events would be served by a messaging or event server,
(something like Kafka, or Azure ServerBus).  Also, the scores that are being
assessed are hard-coded, but we would have a configuration system so that they
could be easily tuned and altered.

---

## Scoring
For my logic, I'm making some assumptions about what might indicate that an event
was likely to be anomalous.  These are discussed briefly below.

Note: I collect the scores as decimal values, but ideally we would normalize the final score
so that it ranged from 0 to 1.0.  What we want is to be able to set the threshold so
that .90 would represent 90% certainty that an event was an anomaly.  As it is, we
would have to play with the scoring to really make it useful.

#### Missing Elements
I am assuming that certain attributes, when missing, are highly correlated with anomalies.
These would include the *ip_domain* and *region*, and to a lesser extent, possibly
*lang* and *country_code*.  I've associated higher scores for *ip_domain* than *lang*,
for example, because it seems to carry more signal.

#### Numeric Elements
Just as with missing attributes, certain attributes, when numeric seem highly correlated
with anomalies. For example, the *ip_domain* seems like it really should not be numeric.

#### User Agent
When the user agent is really long, for example, longer than 300 characters, it seems
very suspicious.  I picked 300 because it seems to carry signal well, but a lower value
is probably warranted.

#### Email
I'm not really sure how valuable email domain is, but it seems that certain domains are
likely to become known as problemsome, so this validator is mainly included here to
show that we can set up whitelists and blacklists that the validators will obey.

#### What it does NOT do
Because of time constraints, the various validators' logic only considers the attributes directly.  
They don't look at any *meta* data.  For example, if we see several events with timestamps very
close to one another, but with other information identical we might call that suspicious.  To
do this we would need some persistent storage (like a database).  Also, in a real system, we would
log the events (again in some kind of DB) so that we can run analytics - for example, if we find
that certain email domains are highly correlated with anomalies we might blacklist them.

---



## To Run:
1. Change directory to the project root, BitlyCodeChallenge.
2. Change directory to bitly and run the main program: python EventAnomalyDetector.py

### Ex: Running the code:
```sh
% git clone https://github.com/hartee/bitly-coding-challenge.git
```
Cloning into 'bitly-coding-challenge'...
...
```sh
% cd bitly-coding-challenge/BitlyCodeChallenge
% ls
```
build
README.md			setup.py
bitly				tests
bitly.egg-info

```sh
% python tests/test_user_agent_validator.py
```
...
\----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK

```sh
% cd bitly
% python EventAnomalyDetector.py
```

Anomaly Detected: score(0.95)
MissingElementValidator: empty ip_domain. Score +0.5
MissingElementValidator: missing lang. Score +0.1
NumericElementValidator: region is numeric: 21. Score +0.35

{"action":"sign_up_finish_google","asn":"AS36947","city":"Skikda","country_code":"DZ","email":"c861b5cc@gmail.com","ip_domain":"","ip_organization":"Algerie Telecom","isp":"Algerie Telecom","latitude":"948411522ce1d7990cb0420b1566c77a38307a3054db7aa18a1edbdbaff2b375","longitude":"1b87e074dd97df3eb61431626c51b5f141ab63f15b9e6325de847c0e82f5962d","network_name":"Telecom Algeria","postal_code":"21005","region":"21","remote_ip":"47b4a039.5ba3ce4f.7bbedd90.b34e2fa4","subregion":"","timestamp":1690261382,"user_agent":"Bitly/2.9.4 (com.bitly.app; build: 1267; Android 33)"}

...

Anomaly Detected: score(1.40)
ActionValidator: action (sign_up_finish_api) is suspicious. Score +0.1
MissingElementValidator: empty city. Score +0.1
MissingElementValidator: empty ip_domain. Score +0.5
MissingElementValidator: empty postal_code. Score +0.1
MissingElementValidator: missing lang. Score +0.1
MissingElementValidator: empty region. Score +0.5

{"action":"sign_up_finish_api","asn":"AS43019","city":"","country_code":"LB","email":"6aaaa20d.bfb055b9@hotmail.com","ip_domain":"","ip_organization":"Farah Net S.a.r.l.","isp":"Farah Net S.a.r.l.","latitude":"e27f28bc99ca8b95e5978d79d1e48df858a757654537f871bed4bde3ac6ba7a1","longitude":"d2bb228bdb64016d44f0729ed584863327abd66be53607f1e1e416164cacd9fe","network_name":"Farah Net S.a.r.l.","postal_code":"","region":"","remote_ip":"911fb450.0ba19c18.a994bb96.f540cccf","subregion":"","timestamp":1690473211,"user_agent":"Bitly/2.9.4 (com.bitly.Bitly; build:1273; iOS 16.5.0) Alamofire/5.0.0-rc.2"}

\---
Results:
\---
Total events:  150374
Total anomalies:  3615
