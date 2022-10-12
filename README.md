<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/ggfunnn/DGCS2EDI">
    <img src="docs/img/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">DGCS2EDI</h3>

  <p align="center">
    Generate invoices in EDI format from DGCS System
    <br />
    <br />
    <a href="https://github.com/ggfunnn/DGCS2EDI/releases">Download</a>
    ·
    <a href="https://github.com/ggfunnn/DGCS2EDI/issues">Report Bug</a>
    ·
    <a href="https://github.com/ggfunnn/DGCS2EDI/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![DGCS2EDI ScreenShot][product-screenshot]](https://github.com/ggfunnn/DGCS2EDI)

This tool allows DGCS System users to generate and mail invoices in EDI format. It works as a "translator" of XML invoices from DGCS System. With one click of a button you can create and send an invoice to a given customer. It makes your and your client life easier.

Here's why:
* You save time on sending an invoice manually
* Your customer saves time thanks to the EDI platform
* Both of you have a transaction history on your e-mail.

Of course this application will never be like an official add-on to DGCS System, but at least it will enable you to use EDI solution.

### Built With

* Python
* Tkinter
* And other tools listed in [acknowledgements](#acknowledgements).



<!-- GETTING STARTED -->
## Getting Started

### Using a standalone file
***Work in progress...*** <br> ~~The recommended method for running the program is to launch it using a standalone file. 
It's available for Windows and macOS users. You can download it [here](https://github.com/ggfunnn/DGCS2EDI/releases).~~

### Linux installation
***Work in progress...*** <br>
~~For Linux users, a tar.gz package with the installation script is available to 
download [here](https://github.com/ggfunnn/DGCS2EDI/releases).~~

### Manual Installation
If you wish to install the program manually, you can do it by cloning the repository directly from GitHub.

#### Prerequisites
To run application you need:

* Python 3.6 or higher
* Tkinter

**Debian/Ubuntu/Linux Mint:**
  ```sh
  sudo apt install -y python3-tk
  ```

**Fedora:**
  ```sh
  sudo dnf install python3-tkinter
  ```

**Arch Linux:**
  ```sh
  sudo pacman -S tk
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/ggfunnn/DGCS2EDI.git
   ```
2. Change your working directory to DGCS2EDI directory
   ```sh
   cd DGCS2EDI
   ```
3. Run application
   ```JS
   python3 run.py
   ```



<!-- USAGE EXAMPLES -->
## Usage
In the "Email Address" field, enter the address where you want the generated invoice to be sent.
In the "Country" field, enter the buyer's country code (for example, PL).
In the "File" field, select the invoice file generated in DGCS System program using the "To File" button.
Finally, click the "Generate" button.

**Warning! Before using the program, please fill in the settings tab.**



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.



<!-- CONTACT -->
## Contact

Jakub Grzesista - [@gg_funnn](https://twitter.com/gg_funnn) - kubagrzesista@gmail.com

Project Link: [https://github.com/ggfunnn/DGCS2EDI](https://github.com/ggfunnn/DGCS2EDI)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Tkinter Designer](https://github.com/ParthJadhav/Tkinter-Designer)
* [py2exe](https://github.com/py2exe/py2exe)
* [py2app](https://github.com/ronaldoussoren/py2app)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)


<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: docs/img/app.png
