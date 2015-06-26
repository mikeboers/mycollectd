mycollectd
==========

It is **my** collectd, not the *other* one.

Periodically collects: ping to Google DNS, battery condition, SMC info (for OS X), and Airport (a.k.a. Apple-centric WiFi) signal strength.


Installation
------------

Dependencies:

~~~
brew cask install smcfancontrol
~~~

Clone this project, then add to `crontab -e`:

~~~
* 0 0 0 0 /path/to/collectd/scripts/collectd-sample -d /path/to/data
~~~


TODO
----

- compress data that no longer matches the pattern
- ingest old adhoc data
