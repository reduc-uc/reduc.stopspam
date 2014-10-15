# reduc.stopspam

`reduc.stopspam` is a series of commands and functions to detect and stop spam
in your local SMTP server, if you are using postfix or zimbra. `reduc.stopspam`
can help you if you are a SMTP provider and want to add an extra layer to avoid
compromised account send spam.


## Instalation

1. Download and install `reduc.stopspam`:

```
git clone git@github.com:reduc-uc/reduc.stopspam.git
cd reduc.stopspam
# type the following command as root user
python setup.py install
```

2. It is recommende to install Dan Berstein's
  [daemontools](http://cr.yp.to/daemontools.html) if you want to run `stopspam`
  as a daemon. If you are using debian or ubuntu:

```
apt-get install daemontools
```

## Usage

`reduc.stopspam` installs the command `stopspam`. `stopspam` offers the
following subcommands:

    General Commands:
      help - Prints the global help message listing all commands.
      serve - Server to detect and suspend accounts that send spam.
    queue Commands:
      postqueue - Gets postfix queue info
      queue-by-senders - List of senders with more entries in the queue
      queue-by-messages - List of senders with more messages to be send
      rmqueue - Remove the messages queued for the given users.
    zimbra Commands:
      zimbra-suspend - Suspends zimbra accounts separates by comma.
      zimbra-reactivate - Reactivates zimbra accounts separated by comma.
      zimbra-status - Prints status of zimbra accounts separated by comma.
    maillog Commands:
      maillog-by-qmgr - List of senders as indicated by qmgr.
      maillog-by-sasl - List of senders as indicated by sasl authentication.

### Queue Commands

These commands operate over postfix's queue.

#### postqueue

Returns a list of the messages in postfix queue. It's equivalent to the command
`postqueue -p` with a different output format.

#### queue-by-senders

Returns a list of the different sender in postfix queue sorted by the number
of entries in the queue.

#### queue-by-messages

Returns a list of the different sender in postfix queue sorted by the number
of messages that will be dispatched (one entry in the queue can have several
destinations).

#### rmqueue

Remove all the messages in postfix queue for the given senders. The senders
can be indicated by repeating the option `-m` or giving a comma separated
value:

```
stopspam rmqueue -m someid -m otherid
stopspam rmqueue -m someid,otherid
```

### Zimbra Commands


#### zimbra-suspend

Suspends the zimbra accounts of the comma-separated list of users

```
stopspam zimbra-suspend someid,otherid
```

#### zimbra-reactivate

reactivates the zimbra accounts of the comma-separated list of users

```
stopspam zimbra-suspend someid,otherid
```

#### zimbra-status

Prints the status of the zimbra accounts of the comma-separated list of users

```
stopspam zimbra-suspend someid,otherid
```

### Maillog Commands

These commands operate over the mail log file.

#### maillog-by-qmgr

Returns a list of the different sender in the mail log file sorted by the
number of entries in the qmge program.

#### maillog-by-sasl

Returns a list of the different sender in the mail log file sorted by the
number of SASL connections.


### General Commands

#### serve

Runs periodically a series of tests to detect and suspend the accounts that
send spam. The server runs in the foreground forever.


## Configuration

`reduc.stopspam` reads its configuration from `/etc/stopspam.cfg`. You can
read `doc/stopspam.cfg` to learn more about the file structure.
