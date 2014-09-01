# The Nu Markup Checker

The Nu Markup Checker is a name for the backend behind
[http://html5.validator.nu][1], [http://validator.w3.org/nu/][2], and the HTML5
facet of the legacy [W3C Validator][3]. Its source code is available from [a set
of repositories hosted at github][4], as is `vnu.jar`, a portable standalone
version for either batch-checking of HTML documents directly from the command
line and from other scripts/apps, or for use as a simple standalone HTTP server
that provides a service for browser-based checking of HTML documents over the
Web—similar to [http://validator.w3.org/nu/][2].

   [1]: http://html5.validator.nu
   [2]: http://validator.w3.org/nu/
   [3]: http://validator.w3.org
   [4]: https://github.com/validator/

The easiest way to do things with the Nu Markup Checker on your own is to [get
the latest vnu.jar release][5].

   [5]: https://github.com/validator/validator.github.io/releases/latest

In the **Usage** section below are instructions on how to use `vnu.jar` to check
the markup of documents.

**Note:** In the instructions, replace _"~/vnu.jar"_ with the actual path to the
`vnu.jar` file on your system.

Alternatively, there’s also now a [Grunt plugin for HTML validation][6] that
uses `vnu.jar` as its backend. You can install that plugin with `npm install
grunt-html --save-dev`.

   [6]: https://github.com/jzaefferer/grunt-html

## Usage

You can use the `vnu.jar` markup checker as an executable for command-line
checking of HTML documents by invoking it like this:

      java -jar ~/vnu.jar [--errors-only] [--no-stream]
           [--format gnu|xml|json|text] [--help] [--html] [--verbose]
           [--version] FILES

To check one or more HTML documents from the command line:

      java -jar ~/vnu.jar FILE.html FILE2.html FILE3.HTML FILE4.html...

**Note:** If you get a `StackOverflowError` error when using the vnu.jar file,
try adjusting the thread stack size by providing the `-Xss` option to java:

      java -Xss512k -jar ~/vnu.jar FILE.html...

To check all HTML documents in a particular directory:

      java -jar ~/vnu.jar some-directory-name/

To check a Web document:

      java -jar ~/vnu.jar _URL_

      example: java -jar ~/vnu.jar http://example.com/foo

To check standard input:

      java -jar ~/vnu.jar -

      example: echo '<!doctype html><title>...' | java -jar ~/vnu.jar -

### Options

When used from the command line as described in this section, the `vnu.jar`
executable provides the following options:

#### --errors-only

    Specifies that only error-level messages and non-document-error messages are
    reported (so that warnings and info messages are not reported).

    default: [unset; all message reported, including warnings & info messages]

#### --format _format_

    Specifies the output format for reporting the results.

    default: "gnu"

    possible values: "gnu", "xml", "json", "text"

    see also:
    [http://wiki.whatwg.org/wiki/Validator.nu_Common_Input_Parameters#out][7]

   [7]: http://wiki.whatwg.org/wiki/Validator.nu_Common_Input_Parameters#out

#### --help

    Shows detailed usage information.

#### --html

    Forces all documents to be parsed by the HTML parser, as text/html
    (otherwise, *.xhtml documents are parsed using an XML parser).

    default: [unset; *.xhtml documents are parsed using an XML parser]

#### --no-stream

    Forces all documents to be be parsed in buffered mode instead of streaming
    mode (causes some parse errors to be treated as non-fatal document errors
    instead of as fatal document errors).

    default: [unset; non-streamable parse errors cause fatal document errors]

#### --verbose

    Specifies "verbose" output. (Currently this just means that the names of
    files being checked are written to stdout.)

    default: [unset; output is not verbose]

#### --version

    Shows the vnu.jar version number.

For details on how to provide browser-based checking of documents over the Web
using either the `vnu.jar` package or an alternative `vnu.war` package that’s
also available, see [Web-based checking with vnu.war or vnu.jar][8].

   [8]: http://validator.github.io/service.html

