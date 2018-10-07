def primary_nav():
    return [("/", "home", "Home"),
            ("/about", "about", "About")]


def patient_nav():
    return [("/patient", "patient", "Home"),
            ("/register", "register", "Register"),
            ("/booking", "booking", "Booking"),
            ("/about", "about", "About")]


def doctor_nav():
    return [("/doctor", "home", "Home"),
            ("/consultation_list", "consultation_list", "Consultation Notes"),
            ("/schedule", "schedule", "Weekly Schedule"),
            ("/about", "about", "About")]


def clerk_nav():
    return [("/clerk", "home", "Home"),
            ("/calendar_all", "calendar_all", "Calendar"),
            ("/consultation_bookings", "consultation_bookings", "Booking List"),
            ("/booking", "booking", "Booking"),
            ("/statistics", "statistics", "Statistics")]
