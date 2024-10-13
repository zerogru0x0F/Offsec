import cmd
import sqlite3
import subprocess
import requests


class ExploitFramework(cmd.Cmd):
    intro = "Welcome to your custom Exploit Framework. Type 'help' or '?' to list commands.\n"
    prompt = "(exploit-framework) "

    def __init__(self):
        super().__init__()
        # Initialize the SQLite database for command history
        self.conn = sqlite3.connect("exploit_framework.db")
        self.cursor = self.conn.cursor()
        # Create a table for storing command history if it doesn't exist
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                output TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        self.conn.commit()

    def do_scan(self, arg):
        """Scan a target IP or domain using nmap. Usage: scan <target> [nmap options]"""
        args = arg.split()
        if len(args) == 0:
            print("[!] Please provide a target to scan.")
            output = "[!] Please provide a target to scan."
        else:
            target = args[0]
            options = args[1:]

            print(f"[*] Scanning {target} with nmap...")
            try:
                cmd = ['nmap', target] + options
                result = subprocess.run(cmd, capture_output=True, text=True)
                output = result.stdout
                print(output)
            except Exception as e:
                output = f"[!] Error running nmap: {e}"
                print(output)

        # Log the command and its output to history
        self.log_command(f"scan {arg}", output)

    def do_dig(self, arg):
        """Scan a target IP or domain using dig. Usage: search <target> [nmap options]"""
        args = arg.split()
        if len(args) == 0:
            print("[!] Please provide a target to dig.")
            output = "[!] Please provide a target to dig."
        else:
            target = args[0]
            options = args[1:]

            print(f"[*] DNS server {target} with dig...")
            try:
                cmd = ['dig', target] + options
                result = subprocess.run(cmd, capture_output=True, text=True)
                output = result.stdout
                print(output)
            except Exception as e:
                output = f"[!] Error running dig: {e}"
                print(output)

        # Log the command and its output to history
        self.log_command(f"dig {arg}", output)

    def do_curl(self, arg):
        """Scan a target IP or domain using curl. Usage: search <target> [nmap options]"""
        args = arg.split()
        if len(args) == 0:
            print("[!] Please provide a target to curl.")
            output = "[!] Please provide a target to curl."
        else:
            target = args[0]
            options = args[1:]

            print(f"[*] Web Application {target} with curl...")
            try:
                cmd = ['curl', target] + options
                result = subprocess.run(cmd, capture_output=True, text=True)
                output = result.stdout
                print(output)
            except Exception as e:
                output = f"[!] Error running curl: {e}"
                print(output)

        # Log the command and its output to history
        self.log_command(f"curl {arg}", output)

    def do_scraping(self, arg):
        """Scan a target IP or domain using request. Usage: scraping <target> [nmap options]"""
        args = arg.split()
        if len(args) == 0:
            print("[!] Please provide a target to Scraping .")
            output = "[!] Please provide a target to Scraping ."
        else:
            target = args[0]
            options = args[1:]

            print(f"[*] Web Application {target} with Scraping ...")
            target = str(target)
            try:
                # Custom headers
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Referer': f'{target}',
                }
                # Send GET request with custom headers
                result = requests.get(target, headers=headers)
                # Check the response
                output = result.text
                print(output)
            except Exception as e:
                output = f"[!] Error running Scraping : {e}"
                print(output)

        # Log the command and its output to history
        self.log_command(f"scraping {arg}", output)

    def do_exploit(self, arg):
        """Exploit a vulnerability on a given target."""
        output = "[*] Exploit functionality not implemented yet."
        print(output)
        self.log_command(f"exploit {arg}", output)

    def do_payload(self, arg):
        """Generate a payload."""
        output = "[*] Payload generation functionality not implemented yet."
        print(output)
        self.log_command(f"payload {arg}", output)

    def do_history(self, arg):
        """Show the most recent 3 commands in the history."""
        print("[*] Command History (recent 3):")
        self.cursor.execute("SELECT * FROM history ORDER BY timestamp DESC LIMIT 3;")
        rows = self.cursor.fetchall()
        if rows:
            for row in rows:
                print(f"{row[0]} | {row[1]} | {row[2]}")  # Show ID, timestamp, command, and output
        else:
            print("[!] No command history found.")

    def do_exit(self, arg):
        """Exit the framework."""
        print("Goodbye!")
        self.conn.close()  # Close the SQLite connection
        return True

    def log_command(self, command, output):
        """Log the command and its output into the SQLite database."""
        self.cursor.execute("INSERT INTO history (command, output) VALUES (?, ?);", (command, output))
        self.conn.commit()

    def default(self, line):
        """Handle unknown commands."""
        print(f"Unknown command: {line}. Type 'help' or '?' for a list of commands.")


# Run the shell
if __name__ == '__main__':
    ExploitFramework().cmdloop()
