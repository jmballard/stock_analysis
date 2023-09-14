from IPython.display import display, HTML
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import yaml
import bs4 as BeautifulSoup


class EmailAlert:
    """This class is to create email alerts.

    extended_summary.
    """

    def __init__(
        self,
    ):
        """Initialise email alert.

        extended_summary.
        """
        graphs = [
            "https://plotly.com/~christopherp/308",
            "https://plotly.com/~christopherp/306",
            "https://plotly.com/~christopherp/300",
            "https://plotly.com/~christopherp/296",
        ]

        template = (
            ""
            '<a href="{graph_url}" target="_blank">'  # Open the interactive graph when you click on the image
            '<img src="{graph_url}.png">'  # Use the ".png" magic url so that the latest, most-up-to-date image is included
            "</a>"
            "{caption}"  # Optional caption to include below the graph
            "<br>"  # Line break
            '<a href="{graph_url}" style="color: rgb(190,190,190); text-decoration: none; font-weight: 200;" target="_blank">'
            "Click to comment and see the interactive graph"  # Direct readers to Plotly for commenting, interactive graph
            "</a>"
            "<br>"
            "<hr>"  # horizontal line
            ""
        )

        email_body = ""
        for graph in graphs:
            _ = template
            _ = _.format(graph_url=graph, caption="")
            email_body += _

        self.email_body = email_body

        self.subject = "test email plotly"

    def show(self):
        display(HTML(self.email_body))

    def write(self):
        with open("outputs/alert.html", "w") as f:
            f.write(self.email_body)

    def send(self, sender, recipient):
        email_server_host = "smtp.gmail.com"
        port = 587
        email_details = yaml.load(
            open("config/email_details.yml", "r"), Loader=yaml.FullLoader
        )
        email_username = email_details["email_username"]
        email_password = email_details["email_password"]

        msg = MIMEMultipart("alternative")
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = self.subject

        msg.attach(MIMEText(self.email_body, "html"))

        server = smtplib.SMTP(email_server_host, port)
        server.ehlo()
        server.starttls()
        server.login(email_username, email_password)
        server.sendmail(sender, recipient, msg.as_string())
        server.close()


if __name__ == "__main__":
    em = EmailAlert()
    em.write()
    # em.send(sender="jmbemailalerts@gmail.com", recipient="bronnimannj@gmail.com", subject="test alert")
