#### install.sh (optional but pro – make it executable on GitHub)
```bash
#!/bin/bash
pkg update -y
pkg install python git -y
pip install telethon rich colorama aiohttp requests pyrogram tgcrypto
echo "Installation complete! Now run: python killertermux.py"
