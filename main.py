import logging
import smtplib
import tkinter as tk
import tkinter.messagebox as messagebox
import csv
from email.message import EmailMessage
from config import SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD

# logging configuration
logging.basicConfig(
    filename="email_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def send_mail(name, rec_mail, subject):
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = rec_mail
        msg["Subject"] = subject
        msg.set_content(f"""Hello {name},
This is a test email sent using Python.

Best Regards,
E-mail Automation System""")

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        logging.info(f"Email sent to {rec_mail} with subject '{subject}' Successfully.!!")
        print(f"Email sent to {rec_mail} with subject '{subject}' Successfully.!!")

        return True, rec_mail   # ✅ FIX

    except Exception as e:
        logging.error(f"Failed to send email to {rec_mail}. Error: {e}")
        print(f"Failed to send email to {rec_mail}. Error: {e}")

        return False, rec_mail  # ✅ FIX


# action ui
def sendn_bulk_emails():
    success_count = 0
    failure_count = 0

    try:
        with open(r"recipients.csv", newline='') as file:
            reader = csv.DictReader(file)

            for row in reader:
                status, email = send_mail(
                    row["name"],
                    row["email"],
                    row["subject"]
                )

                if status:
                    success_count += 1
                    status_label.config(text=f"Emails Sent Successfully: {success_count}")
                else:
                    failure_count += 1
                    status_label.config(text=f"Emails Failed: {failure_count}")

                root.update()

            messagebox.showinfo(
                "Email Sending Completed",
                f"Emails Sent Successfully: {success_count}\nEmails Failed: {failure_count}"
            )

    except FileNotFoundError:
        messagebox.showerror("Error", "recipients.csv file not found.")


# ui
root = tk.Tk()
root.title("E-mail Automation System")
root.geometry("400x200")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="E-mail Automation System",
    font=("Helvetica", 16, "bold")
)
title_label.pack(pady=10)

send_button = tk.Button(
    root,
    text="Send Emails",
    font=("Helvetica", 14),
    bg="#4CAF50",
    fg="white",
    width=15,
    command=sendn_bulk_emails
)
send_button.pack(pady=20)

status_label = tk.Label(
    root,
    text="Status: Waiting...",
    font=("Helvetica", 12)
)
status_label.pack(pady=10)

exit_button = tk.Button(
    root,
    text="Exit",
    font=("Helvetica", 12),
    bg="#f44336",
    fg="white",
    width=10,
    command=root.destroy
)
exit_button.pack(pady=10)

root.mainloop()
