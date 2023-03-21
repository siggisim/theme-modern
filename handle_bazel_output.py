import re
import sys

defaultGreen = "\x1b[32m"
brightGreenBold = "\x1b[92;1m"
brightCyanBold = "\x1b[96;1m"
yellow = "\x1b[93m"
red = "\x1b[91m"
redBold = "\x1b[91;1m"
brightWhiteBoldUnderline = "\x1b[37;1;4m"
brightWhiteBold = "\x1b[37;1m"
bold = "\x1b[1m"
grey = "\x1b[90m"
reset = "\x1b[0m"

startingMessage = "Starting local Bazel server and connecting to it..."

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.replace(startingMessage, grey+startingMessage+reset)
        line = line.replace(defaultGreen+"INFO", brightGreenBold+"INFO")
        line = line.replace(defaultGreen+"Loading", brightGreenBold+"Loading")
        line = line.replace(defaultGreen+"Analyzing", brightGreenBold+"Analyzing")
        line = line.replace("Build did NOT complete successfully", "Build did NOT complete successfully ❌")
        line = line.replace("Build completed successfully, ", "Build completed successfully ✅ ")
        line = line.replace("Starting clean.", "Starting clean 🧽")
        line = line.replace("build interrupted", "build interrupted 😡")
        line = line.replace(defaultGreen+"[", brightGreenBold+"[")

        m = re.search(r"^([\s]*)\s\s([^\s]*)(\s?.*)(; )([0-9]+)s(.*)$", line)
        if m:
            numColor = grey
            if int(m.group(5)) >= 5:
                numColor = yellow
            if int(m.group(5)) >= 20:
                numColor = red
            if int(m.group(5)) >= 60:
                numColor = redBold
            emoji = "🔨"
            if " remote" in m.group(6):
                emoji = "⚡️"
            print(m.group(1)+emoji+" "+brightWhiteBold+m.group(2)+reset+m.group(3)+grey+m.group(4)+numColor+m.group(5)+"s"+grey+m.group(6)+reset)
            continue

        m = re.search(r"^(.*Streaming build results to: )(.*)$", line)
        if m:
            print(m.group(1)+brightWhiteBoldUnderline+m.group(2)+reset)
            continue

        m = re.search(r"^(.*Elapsed time: )([0-9\.]+s)(, Critical Path: )([0-9\.]+s)(.*)$", line)
        if m:
            print(m.group(1)+brightWhiteBold+m.group(2)+" ⏳"+reset+m.group(3)+brightWhiteBold+m.group(4)+" ⏰"+reset+m.group(5))
            continue
        
        print(line, end="")
