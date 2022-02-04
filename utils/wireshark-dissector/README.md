# PolKA Wireshark Dissector
Wireshark dissector for Polynomial Key-based Architecture for Source Routing (PolKA) is written in Lua programming language, and it was tested in Wireshark versions 3.4 and 3.6.

## How to Install PolKA Wireshark Dissector on macOS

1 - Go to the about menu and then folders

![Screen Shot 2022-01-19 at 13 27 40](https://user-images.githubusercontent.com/56919528/150174090-0b94ce3e-9287-4e88-90da-03ba76df210c.png)

2 - Then, put the polka dissector in the Lua plugins folder

![Screen Shot 2022-01-19 at 14 00 36](https://user-images.githubusercontent.com/56919528/150178502-39229eab-4acb-42b1-a6e8-fba60580eb0e.png)

3 - Next step is to go to the preferences panel and add the polka dissector in DLT USER

![Screen Shot 2022-01-19 at 13 40 12](https://user-images.githubusercontent.com/56919528/150175895-0993b5e7-613a-4f5c-853d-ebe012619d16.png)

![Screen Shot 2022-01-19 at 13 40 36](https://user-images.githubusercontent.com/56919528/150175940-ab3b82ce-9aec-411f-a01c-0f5424f2793e.png)

4 - Go to the Analyze menu and reload Lua plugins

![Screen Shot 2022-01-19 at 13 48 54](https://user-images.githubusercontent.com/56919528/150176440-02f1a264-b810-4b28-924c-2a6bc2d55a20.png)

5 - Open the pcap file, ready now, explore and enjoy
 ![Screen Shot 2022-01-19 at 13 51 33](https://user-images.githubusercontent.com/56919528/150177287-92604673-1d50-4de7-a730-b6cd517d95ee.png)

## How to Install PolKA Wireshark Dissector on Linux

### Create the LUA Plugin folder on Wireshark
`Help` > `About` > `Folders` > Click on `Personal Lua Plugins`

### Or create manualy the LUA Plugin folder
```zsh
mkdir /home/$USER/.local/lib/wireshark/plugins
```

### Download the PolKA Wireshark Dissector 
```zsh
cd /home/$USER/.local/lib/wireshark/plugins
wget https://raw.githubusercontent.com/nerds-ufes/polka/main/utils/wireshark-dissector/polka_dissector.lua
```

### Reload LUA Plugins
`Analyze > Reload LUA Plugins` or `Ctrl + Shift + L`

### Next step go to the preferences panel and add the polka dissector in DLT USER (as shown on Mac OS)
`Edit` > `Preferences` or `Ctrl + Shift + P`

# Conclusion
In this code you:

The code makes it easier to view the polka package through Wireshark.

# References
- https://ieeexplore.ieee.org/document/9165501

- https://chalk-thought-7ce.notion.site/PolKA-Project-7452bbe9bd294a9b88791ba9650a7069

- https://osqa-ask.wireshark.org/

- https://stackoverflow.com/
