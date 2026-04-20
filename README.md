# Event Planner Application

A desktop-based Event Planning Application developed using Python (Tkinter and Pillow). The application enables users to plan and customize events such as weddings, birthdays, and corporate events with theme selection, food packages, and cost estimation.

---

## Features

* Multiple event types:

  * Wedding
  * Birthday
  * Corporate events

* Theme and event selection:

  * Lavish, Traditional, Hybrid (Wedding)
  * Theme Party, Glamourous (Birthday)
  * AGM, Award Function, Fresher’s Party (Corporate)

* Food package options:

  * Basic
  * Elite
  * Premium

* Guest count input for dynamic pricing

* Automatic cost calculation:

  * Event cost + Food cost = Total cost

* Booking summary and confirmation screen

* Interactive graphical user interface with images and hover effects

---

## Tech Stack

* Python
* Tkinter (GUI framework)
* Pillow (image processing)

---

## Project Structure

Event-Planner/
│── latest.py
│── image files
│── README.md

---

## Installation and Setup

1. Clone the repository

```bash
git clone https://github.com/your-username/event-planner.git
cd event-planner
```

2. Install dependencies

```bash
pip install pillow
```

3. Run the application

```bash
python latest.py
```

---

## Required Image Files

Ensure the following files are present in the same directory as `latest.py`:

* background2.png
* background4.jpeg
* background6.jpeg
* birthdayback.jpeg
* theme.jpeg
* elegant.jpeg
* agm.jpeg
* award.jpeg
* corpfood.jpeg
* freshers.jpeg
* birthday.png
* corporate.png
* wedding2.png
* traditional2.jpeg
* posh2.jpeg
* hybrid.jpeg

---

## How It Works

1. Select an event type
2. Choose a theme or event category
3. Select a food package
4. Enter number of guests
5. View total cost
6. Confirm booking

---

## Notes

* File names are case-sensitive
* Missing images may affect UI rendering
* Guest input must be a valid number

---

## Future Enhancements

* Database integration for storing bookings
* Export booking summary as PDF
* User authentication system
* Payment gateway integration
* Migration to web-based platform

---

## License

This project is intended for educational use and can be modified freely.
