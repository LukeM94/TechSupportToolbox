# Tech Support Toolbox

A cross-platform command-line network diagnostic tool for IT professionals. Perform common network troubleshooting tasks from a single, colorful, easy-to-use interface.

## Features

- 🌐 **Cross-Platform Support** - Works on Windows, macOS, and Linux
- 🎨 **Colourised Output** - Easy-to-read, colour-coded terminal output
- 💾 **Save Results** - Option to save command outputs to timestamped files
- 🔒 **Input Validation** - Built-in protection against command injection

## Available Tools

1. **Ping** - Test network connectivity to a host
2. **Network Config** - Display network interface configuration
3. **MAC Address** - Show MAC addresses for network interfaces
4. **DNS Lookup** - Perform DNS resolution (nslookup)
5. **Traceroute** - Trace the route packets take to a destination
6. **Port Scanner** - Check if a specific port is open on a host
7. **Network Interfaces** - List all network interfaces with details

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/LukeM94/TechSupportToolbox.git
cd TechSupportToolbox
```

2. Run the tool:
```bash
python3 pingy.py
```

## Usage

Simply run the script and follow the interactive menu:

```bash
python3 pingy.py
```

Select a tool by entering its number (1-7) or name, then follow the prompts.

### Examples

**Ping a host:**
```
Type an option: 1
Enter an IP address or hostname to ping: google.com
```

**Check if a port is open:**
```
Type an option: 6
Enter an IP address or hostname: 192.168.1.1
Enter port number: 80
```

**Save output to file:**
After any command completes, you'll be prompted:
```
Save output to file? (y/n): y
```

## Development

### Running Tests

Install pytest:
```bash
pip3 install pytest
```

Run the test suite:
```bash
python3 -m pytest test_pytest.py -v
```

### Project Structure

```
TechSupportToolbox/
├── pingy.py           # Main application
├── test_pytest.py     # Test suite
├── README.md          # This file
├── LICENSE            # MIT License
└── .gitignore         # Git ignore rules
```

## Platform-Specific Notes

The tool automatically detects your operating system and uses the appropriate commands:

- **Windows**: `ping -n`, `ipconfig`, `getmac`, `tracert`
- **macOS**: `ping -c`, `ifconfig`, `traceroute`
- **Linux**: `ping -c`, `ip addr`, `traceroute`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Luke Morton** - [LukeM94](https://github.com/LukeM94)