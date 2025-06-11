# CSS Selector Generator

This project provides a command-line tool that extracts the most stable CSS selector from an HTML snippet. A small web interface is also included for interactive use.

## Requirements

* Python 3
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
* [Flask](https://flask.palletsprojects.com/)

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Command Line Usage

Generate a selector from a file:

```bash
python css_selector_generator.py path/to/file.html
```

If no file is provided, HTML is read from standard input.

## Web Interface

Start the Flask app to use a simple web interface:

```bash
python web_interface.py
```

Open `http://localhost:5000` in your browser, paste HTML into the textbox, and the tool will display the generated selector.
