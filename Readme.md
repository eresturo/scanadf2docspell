# scanadf2docspell

This script scans from the ADF (Automatic Document Feeder), preprocesses it and uploads
it to Docspell.

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f3370d96dd974f419b9d23c7fb0f2f22)](https://www.codacy.com/gh/eresturo/scanadf2docspell/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=eresturo/scanadf2docspell&amp;utm_campaign=Badge_Grade)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=eresturo_scanadf2docspell&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=eresturo_scanadf2docspell)
[![CodeFactor](https://www.codefactor.io/repository/github/eresturo/scanadf2docspell/badge)](https://www.codefactor.io/repository/github/eresturo/scanadf2docspell)
[![Known Vulnerabilities](https://snyk.io/test/github/eresturo/scanadf2docspell/badge.svg)](https://snyk.io/test/github/eresturo/scanadf2docspell)
[![MegaLinter](https://github.com/eresturo/scanadf2docspell/actions/workflows/mega-linter.yml/badge.svg)](https://github.com/eresturo/scanadf2docspell/actions/workflows/mega-linter.yml)

![Overview](overview.png)

## Prerequisites

* A running [Docspell](https://github.com/eikek/docspell) instance.
* Any Linux distro (tested on Ubuntu 20.04)
* Install system requirements (apt command on Ubuntu:)

  ```bash
  sudo apt install sane python3 python3-pip libmagickwand-dev img2pdf sane-utils
  ```

* See if [scanimage](https://linux.die.net/man/1/scanimage) is able to find your scanner

  ```bash
  scanimage -L
  ```

  * if scanner is not found -> check `sane-find-scanner`
    * Maybe also as sudo to see if it's an privileges problem
    * If yes try `sudo adduser <username> lp` and logout/login and restart scanner

## Install

* Clone the repository

  ```bash
  git clone https://github.com/eresturo/scanadf2docspell
  ```

* Install requirements

  ```bash
  cd scanadf2docpsell
  pip3 install -r requirements.txt
  ```

* Generate a API-Key, as
  described [here](https://docspell.org/docs/webapp/uploading/#anonymous-upload)
* create a config file `custom.conf`

  ```yaml
  api_key: 'YOUR_API_KEY'
  docspell_url: 'http://YOUR_DOCSPELL_URL'
  ```

### Scanner specific adjustments

Unfortunately, `scanimage` arguments are partially dependent on the scanner. Therefore,
a customized configuration per
scanner may be necessary. For this purpose, you can specify with which command a
flatbed, with which a single-page adf
scan and with which a duplex adf scan can be triggered.

<!-- markdownlint-disable no-inline-html -->

| tested Scanners        | Config `(custom.conf)`                                                                                                                                                                              |
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Epson XP 860 (default) | `command_flatbed: '--source Flatbed'`<br>`command_adf: '--source "Automatic Document Feeder" --adf-mode Simplex'`<br>`command_duplex_adf: '--source "Automatic Document Feeder" --adf-mode Duplex'` |
| HP 5590                | `command_flatbed: '--source Flatbed'`<br>`command_adf: '--source ADF'`<br>`command_duplex_adf: '--source "ADF Duplex"'`                                                                             |

<!-- markdownlint-enable no-inline-html -->

**Note**: This list is far from complete. Which scanner do you use and which
configuration is needed? Please tell us in
an issue or pull request.

## Scan

* insert a document in your scanner and run

  ```bash
  ./scan.py
  ```

* See help for further options.

  ```bash
  ./scan.py --help
  ```

## Contribution

Suggestions, feature requests, ideas to improve the script? Feel free to open an issue
or send a pull request :)
