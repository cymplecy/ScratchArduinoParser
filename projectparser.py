__author__ = 'Simon'
#!/usr/bin/env python
# projectparse - convert .sb2 project files into Arduino code.
#Copyright (C) 2014 by Simon Walters

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

codeInput = []
codeOutput = []

with open("project.txt","r") as projectFile:
    codeInput = projectFile.readlines()
for line in codeInput:
    print line

print
print "converts to"
print

indent = ""
state = ""
pinsOut  = []

for line in codeInput:
    line = line.lower()
    if "forever" in line:
        codeOutput.append("void loop() {")
        indent += "    "
    if  "broadcast" in line:
        if "pin" in line:
            if "on" in line:
                state = "HIGH"
                value = line[line.find("pin") + 3:line.find("on")]
                if value not in pinsOut:
                    pinsOut.append(value)
                codeOutput.append(indent + "digitalwrite (" + value + "," + state + ");")
            if "off" in line:
                state = "LOW"
                value = line[line.find("pin") + 3:line.find("off")]
                if value not in pinsOut:
                    pinsOut.append(value)
                codeOutput.append(indent + "digitalwrite (" + value + "," + state + ");")
    if  "wait" in line:
        if "(" in line:
            value = line[line.find("(") + 1:line.find(")")]
            codeOutput.append(indent + "delay (" + str(int(float(value) * 1000)) + ");")
    if  "end" in line:
        indent = indent[:-4]
codeOutput.append("}")


if pinsOut != []:
    codeOutput.insert(0,"void setup() {")
    for pin in pinsOut:
        codeOutput.insert(1,"    pinMode(" + pin + ", OUTPUT);")
    codeOutput.insert(len(pinsOut) + 1,"}")

print
for line in codeOutput:
    print line