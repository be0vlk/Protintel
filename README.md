# PROTINTELLIGENCE 🕵🏻‍♂️
**ProtINTelligence** is a Python script for the **OSINT &amp; Cyber Community**. This repo is a fork of the original project by C3n7ral051nt4g3ncy. It's main changes are enchanced usability by accepting command line arguments and files as input.<br>


## What can this tool do so far? 
  
**Protintelligence is currently working perfectly for checking any domain** to see if this domain uses protonmail to send and receive emails.
<br>
Input example: ```test@fornever.me```
  
<br>
  
With the input above, this tool will be able to:
   - **Confirm** if the custom domain uses Protonmail to send and receive emails
   - **Detect** if the custom domain is using a **catch-all** and provide you with the main email address.
   - **Provide** you with PGP key creation date and time (This is often the same date & time as account creation because not many people change their keys)
   - **Provide** the Key Encryption Type: RSA	or ECC (Curve25519)
   - **Get** PGP Key information + creation date and time for any protonmail email address (protonmail.ch, protonmail.com, proton.me, pm.me)
  
  ⚠️ Make sure the protonmail address exists because the protonmail API response to non-valid email addresses also shows PGP key with a randomized creation date and time.
  
  
## Requirements
[Python 3](https://www.python.org/downloads/)<br>


## Installation ⚙️

```
git clone https://github.com/be0vlk/Protintel
```

```
cd Protintel
```

```
pip3 install -r requirements.txt depending on your set-up.
```

## Usage

This fork adds functionality to use CLI arguments, like so:
```
python3 protintel.py justanexample@proton.me
```

Or multiple addresses:

```
python3 protintel.py justanexample@proton.me justanexample2@proton.me justanexample3@proton.me
```

Or a file as input:

```
python3 protintel.py emails.txt
```

Or even multiple files:

```
python3 protintel.py emails.txt emails.csv emails.html
```

## Disclaimer ⚠️

`This tool is for the OSINT and Cyber community, don't use it for wrong, immoral, or illegal reasons. I am not responsible for any damage that you cause.`

## License ⚖️
[MIT](https://choosealicense.com/licenses/mit/)
