# KILLER KING 😈👑 - Ultimate Telegram Ban Tool
# Owner: @killerking20000 | Termux God

import asyncio
import os
import random
import time
import smtplib
import requests
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from colorama import init
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
from rich import box
import subprocess
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)
console = Console()

#  CONFIG 
GITHUB_REPO = "https://github.com/K1llerK1ng2000/killer-reports.git"
REPO_DIR = "killer-reports"
PROXY_FILE = "working_proxies.txt"
TARGET_PROXY_COUNT = 500
MAX_REPORTS = 500
os.makedirs(REPO_DIR, exist_ok=True)

# YOUR EMAILS
SMTP_ACCOUNTS = [
    ("ana12juli13@gmail.com", "teqlhggnfyoclnvh"),
    ("elizabeth1mary2@gmail.com", "axwmdyhwdtmpvjjj"),
    ("k1llerking1048@gmail.com", "ivrpoetevxdfgnbr"),
    ("juli12ana13@gmail.com", "drpfaafwxtefqypq"),
    ("mary12eli34@gmail.com", "dqjchqtuzmtihmpu"),
    ("he19rry89@gmail.com", "zivbxunrghnltskn"),
    ("mrmaguire475@gmail.com", "losuseiozvhawbyo"),
    ("mr12john21@gmail.com", "resybaosyofssaia"),
    ("golliblegreg@gmail.com", "bgqmhigbekmoxxqx"),
]

WEB_URLS = ["https://telegram.org/support", "https://telegram.org/abuse", "https://telegram.org/dsa-report"]

#  PROXY MASTER 
class ProxyMaster:
    def __init__(self):
        self.sources = [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
            "https://api.openproxylist.xyz/http.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://multiproxy.org/txt_all/proxy.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        ]

    def get_proxy(self):
        if os.path.exists(PROXY_FILE) and os.path.getsize(PROXY_FILE) > 100:
            proxies = [l.strip() for l in open(PROXY_FILE) if l.strip()]
            return random.choice(proxies) if proxies else None
        return None

    def test_proxy(self, proxy):
        try:
            proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            requests.get("http://httpbin.org/ip", proxies=proxies, timeout=8)
            return True
        except:
            return False

    def harvest_and_save(self):
        console.print("\n[bold red]DELETING OLD PROXIES & STARTING FRESH HUNT...[/]")
        if os.path.exists(PROXY_FILE):
            os.remove(PROXY_FILE)

        console.print("[bold yellow]STEP 1: FETCHING MASSIVE PROXY LIST (50K–200K+)...[/]")
        all_proxies = set()
        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = [executor.submit(requests.get, url, timeout=25) for url in self.sources]
            for future in futures:
                try:
                    text = future.result().text
                    found = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}', text)
                    all_proxies.update(found)
                except: pass

        proxy_list = list(all_proxies)
        random.shuffle(proxy_list)
        console.print(f"[bold green]SUCCESS: Collected {len(proxy_list):,} raw proxies![/]")

        console.print(f"\n[bold yellow]STEP 2: TESTING PROXIES → WILL STOP AT {TARGET_PROXY_COUNT} WORKING[/]")
        working = 0
        with Progress() as progress:
            task = progress.add_task("[red]Testing Proxies...", total=TARGET_PROXY_COUNT)
            with ThreadPoolExecutor(max_workers=120) as executor:
                for proxy in proxy_list:
                    if working >= TARGET_PROXY_COUNT:
                        break
                    if executor.submit(self.test_proxy, proxy).result():
                        working += 1
                        with open(PROXY_FILE, "a") as f:
                            f.write(proxy + "\n")
                        progress.update(task, advance=1)
                        speed = working / (time.time() - start_time + 1)
                        progress.console.print(f"[green]Working: {working}/{TARGET_PROXY_COUNT} | Speed: {speed:.1f}/sec[/]")

        console.print(Panel(f"[bold green]500 WORKING PROXIES SAVED SUCCESSFULLY!\nFile: {PROXY_FILE}[/]", title="PROXY HUNT COMPLETE"))
        console.input("\n[bold cyan]Press Enter to continue to main menu...[/]")

proxy_master = ProxyMaster()

# MESSAGES & REPORTERS 
def pull_messages():
    console.print(Panel("[bold cyan]Updating report messages from GitHub...", title="Sync"))
    if os.path.exists(REPO_DIR):
        subprocess.run(["rm", "-rf", REPO_DIR], stdout=subprocess.DEVNULL)
    subprocess.run(["git", "clone", "--depth=1", GITHUB_REPO, REPO_DIR], stdout=subprocess.DEVNULL)
    console.print("[bold green]Messages updated![/]")
    console.input("[cyan]Press Enter...[/]")

def load_messages():
    msgs = {}
    files = {"user": "user_report_messages.txt", "channel": "channel_report_messages.txt", "group": "group_report_messages.txt"}
    for k, f in files.items():
        path = os.path.join(REPO_DIR, f)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as file:
                lines = [l.strip() for l in file if l.strip()]
                msgs[k] = lines or ["This account spreads illegal content."]
        else:
            msgs[k] = ["Spam and scam."]
    return msgs

def get_fake_reporter():
    names = ["Ahmed Khan", "John Smith", "Ali Hassan", "Maria Garcia", "Omar Ali"]
    phones = ["+923001234567", "+19876543210", "+447700900987", "+919876543210", "+201234567890"]
    return random.choice(names), random.choice(phones)

# REPORT FUNCTIONS 
async def send_email_report(target, reason, message):
    email, pwd = random.choice(SMTP_ACCOUNTS)
    name, phone = get_fake_reporter()
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = "abuse@telegram.org"
    msg['Subject'] = f"URGENT: {reason.upper()} - @{target}"
    msg.attach(MIMEText(f"Name: {name}\nPhone: {phone}\nTarget: @{target}\n\n{message}\n\nBAN NOW.", 'plain'))
    try:
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(email.split("@")[0], pwd)
        s.sendmail(email, "abuse@telegram.org", msg.as_string())
        s.quit()
        console.print(f"[green]EMAIL SENT → {name}[/]")
        return 1
    except:
        return 0

def send_web_report_via_proxy(target, reason):
    proxy = proxy_master.get_proxy()
    if not proxy: return 0
    try:
        requests.get(random.choice(WEB_URLS), params={"target": f"@{target}"}, 
                    proxies={"http": f"http://{proxy}"}, timeout=8)
        console.print(f"[magenta]WEB REPORT → {proxy.split(':')[0]}[/]")
        return 1
    except:
        return 0

async def report_cmd(rtype):
    target = console.input(f"[bold yellow]Target @{rtype}: [/]").strip().lstrip("@")
    if not target: 
        console.input("Invalid. Press Enter...")
        return

    amount = int(console.input(f"[bold yellow]Amount (1-{MAX_REPORTS}): [/]") or "100")
    if not 1 <= amount <= MAX_REPORTS:
        console.print(f"[red]Max {MAX_REPORTS}![/]")
        console.input("Press Enter...")
        return

    reason = console.input("[bold yellow]Reason: [/]") or "spam"

    console.print(Panel(f"TARGET: @{target}\nAMOUNT: {amount}\nREASON: {reason}", title="CONFIRM ATTACK"))
    if console.input("[bold red]Start? (yes/no): [/]").lower() not in ["yes", "y"]:
        console.input("[yellow]Cancelled. Press Enter...")
        return

    sent = 0
    with Progress() as p:
        task = p.add_task("[red]DESTROYING TARGET...", total=amount)
        for i in range(amount):
            msg = random.choice(MESSAGES.get(rtype, ["Illegal content"]))
            if i < amount//2:
                sent += await send_email_report(target, reason, msg)
            else:
                sent += send_web_report_via_proxy(target, reason)
            p.update(task, advance=1)
            await asyncio.sleep(random.uniform(1.0, 3.0))

    console.print(Panel(f"[bold green]TARGET REPORTED!\nTELEGRAM SUPPORT TEAM WILL REVIEW THE TARGE AND TAKE ACTIONS LESS THAN 24 HOURS\n{sent}/{amount} REPORTS SENT[/]", title="MISSION SUCCESS"))
    console.input("[bold green]Press Enter to return...[/]")

# MAIN MENU
async def main():
    global MESSAGES, start_time
    start_time = time.time()

    pull_messages()
    MESSAGES = load_messages()

   
    if not os.path.exists(PROXY_FILE) or os.path.getsize(PROXY_FILE) == 0:
        proxy_master.harvest_and_save()
    else:
        count = len([l for l in open(PROXY_FILE) if l.strip()])
        console.print(f"[bold green]Loaded {count} saved proxies![/]")
        console.input("[cyan]Press Enter to continue...[/]")

    while True:
        os.system("clear")
        console.print(Panel("""
[bold red] 
  ██╗  ██╗██╗██╗     ██╗     ███████╗██████╗ 
  ██║ ██╔╝██║██║     ██║     ██╔════╝██╔══██╗
  █████╔╝ ██║██║     ██║     █████╗  ██████╔╝
  ██╔═██╗ ██║██║     ██║     ██╔══╝  ██╔══██╗
  ██║  ██╗██║███████╗███████╗███████╗██║  ██║
  ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
   [bold yellow]THE TERMUX KING[/]
        """, title="KILLER TG BAN", box=box.DOUBLE))

        menu = [
            "1 → Scrape Members", "2 → Add Members", "3 → Report User",
            "4 → Report Channel", "5 → Report Group", "6 → HARD Report",
            "7 → Check Ban", "8 → Protect ID", "9 → Update Messages",
            "99 → Refresh Proxies", "0 → Exit"
        ]
        for item in menu:
            console.print(f"[magenta]{item}[/]")

        choice = console.input("\n[bold green]Choose: [/]").strip()

        if choice == "3": await report_cmd("user")
        elif choice == "4": await report_cmd("channel")
        elif choice == "5": await report_cmd("group")
        elif choice == "9": pull_messages()
        elif choice == "99":
            proxy_master.harvest_and_save()  
        elif choice in ["0", "exit", "q"]:
            console.print("[bold red]THE KING HAS LEFT THE BATTLEFIELD[/]")
            break
        else:
            console.print("[yellow]Coming soon...[/]")
            console.input("[cyan]Press Enter to continue...[/]")

if __name__ == "__main__":
    asyncio.run(main())
